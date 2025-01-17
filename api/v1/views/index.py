#!/usr/bin/python3
"""Displays blueprint pages"""
from api.v1.views import app_views
from flask import jsonify
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/status')
def app_status():
    """method app_status"""
    dictStatus = {"status": "OK"}
    return dictStatus


@app_views.route("/stats")
def obj_count():
    """Count objects by its type"""
    from models import storage

    m_new_dict = {"amenities": Amenity, "cities": City,
                  "places": Place, "reviews": Review,
                  "states": State, "users": User}
    cls_dict = {}
    for key, value in m_new_dict.items():
        counter = storage.count(value)
        cls_dict[key] = counter

    return cls_dict
