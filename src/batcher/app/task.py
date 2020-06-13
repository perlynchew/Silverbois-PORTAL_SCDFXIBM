from __future__ import absolute_import
from app.celeryapp import app
import time
import requests
import json
import os

@app.task
def fire(event_id, location, description):
    payload = {"event_id": event_id, "event": "fire", description": description, "location": location} 
    try:
        upload = requests.post('http://myResponder:5000/event', json=payload, timeout=60)
    except Exception as err:
        raise f'Error occurred: {err}'
    return 'Incident uploaded'


@app.task
def EMS(event_id, location, description):
    payload = {"event_id": event_id, "event": "EMS", "description": description, "location": location}
    try:
        upload = requests.post('http://myResponder:5000/event', json=payload, timeout=60)
    except Exception as err:
        raise f'Error occurred: {err}'
    return 'Incident uploaded'
