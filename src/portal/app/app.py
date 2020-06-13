from flask import Flask, render_template, request
from models import *
from pprint import pprint
import uuid
import json
import os

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "hello!"

# function receives POST requests from AI and inserts in postgres
@app.route("/request", methods=['POST'])
def input():
    try:
        input = request.get_json(force=True)
    except Exception as err:
        return 'Invalid data', 404
    # amend dictionary keys according to json input keys
    event = input.get("event")
    location = input.get("location")
    description = input.get("description")
    # column names matched to postgres table. to add/edit columns, go to models.py
    newtask = Scdf(event=event, location=location, event_id=str(uuid.uuid4()), description=description)
    session.add(newtask)
    session.commit()
    return (f'Received event')

# function to view event status
@app.route("/status")
def view_status():
    results = session.query(Scdf).all()
    current_tasks = []
    for task in results:
        dictret = dict(task.__dict__)
        # SQLAlchemy adds '_sa_instance_state' when converting to dictionary
        dictret.pop('_sa_instance_state', None)
        # "date_done" is in date time format
        dictret["date_done"] = str(dictret.get("date_done"))
        if dictret["status"] is None:
            dictret["status"] = 'STARTED'
        # result in hex has weird leading characters. attempting to remove leading characters
        elif dictret["status"] == 'FAILURE':
            dictret["result"] = 'Error Occured'
        else:
            try:
                result_hex = dictret.get("result").replace('942e', '').split('000000000000008c')[1]
            except Exception as err:
                dictret["result"] = "Result not ready"
            else:
                try:
                    decoded = list(bytes.fromhex(result_hex).decode())
                except Exception:
                    dictret['result'] = "Result cannot be decoded"
                else:
                    dictret['result'] = ''.join(map(str, decoded[1:]))
        current_tasks.append(dictret)
    return (json.dumps(current_tasks, sort_keys=True, indent=4))


@app.route("/accept", methods=['POST'])
def accept():
    try:
        result = request.get_json(force=True)
    except Exception as err:
        return 'invalid data', 404
    session.query(Scdf).filter(Scdf.event_id==result.get("event_id")).update({"CFR": "accepted"})
    session.commit()
    return 'Updated'

app.run(debug=True,host='0.0.0.0')
