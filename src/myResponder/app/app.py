from flask import Flask, render_template, request
from pprint import pprint
import requests
import uuid
import json
import os

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "hello!"

# to stimulate the myResponder API
@app.route("/event", methods=['POST'])
def incident_uploader():
    try:
        event = request.get_json(force=True)
    except Exception as err:
        return ('Invalid data', 404)
    return ('', 204)

# in the event a responder accepts event, notify portal
@app.route("/<event_id>/accept")
def accept_event(event_id):
    payload = {"event_id": event_id}
    send = requests.post('http://portal:5000/accept', json=payload, timeout=60)
    if send.status_code == 200:
        return 'accepted!'
    else: 
        return ('accept fail', 404)


app.run(debug=True,host='0.0.0.0')
