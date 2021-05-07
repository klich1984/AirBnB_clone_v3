#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
import json


@app_views.route('/status')
def app_status():
    """method app_status"""
    dictStatus = {"status": "OK"}
    jsonStatus = json.dumps(dictStatus)
    return jsonify(jsonStatus)