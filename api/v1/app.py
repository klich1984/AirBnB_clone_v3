#!/usr/bin/python3
"""init flask aplication"""
from flask import Flask, Blueprint, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv
import json


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_app(error):
    """method teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """Handles not found errors"""
    err_dict = {"error": "Not found"}
    return make_response(jsonify(err_dict), 404)


if __name__ == "__main__":
    """Runs a flask application"""
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.run(host=host, port=port, threaded=True)
