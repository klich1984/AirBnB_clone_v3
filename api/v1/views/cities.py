#!/usr/bin/phyton3
"""REST full view for cities objects"""
from flask import Flask, abort, jsonify, make_response
from flask import request
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def cities_from_state(state_id=None):
    """Retrieves all cities from a state"""

    states_dict = storage.all(State)
    cities_dict = storage.all(City)
    cities_list = []

    my_state_obj = storage.get(State, state_id)

    if my_state_obj is not None:
        for class_id, class_dict in cities_dict.items():
            if state_id == class_dict.state_id:
                city_obj = storage.get(City, class_dict.id)
                cities_list.append(city_obj.to_dict())
        return (jsonify(cities_list))
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE"])
def city_get_id(city_id=None):
    """Retrieves a city by its id"""

    cities_dict = storage.all(City)

    for c_id, city_objs in cities_dict.items():
        if city_id == city_objs.id:
            if request.method == "GET":
                return jsonify(city_objs.to_dict())

            elif request.method == "DELETE":
                storage.delete(city_objs)
                return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def city_create(state_id=None):
    """Creates a city within a state by its id"""

    states_dict = storage.all(State)
    cities_dict = storage.all(City)
    cities_list = []

    my_state_obj = storage.get(State, state_id)

    if my_state_obj is not None:
        my_json = request.get_json(silent=True)
        if my_json is not None:
            if "name" in my_json:
                name = my_json["name"]
                new_city = City(name=name, state_id=state_id)
                new_city.save()
                return make_response(jsonify(new_city.to_dict()), 201)
            else:
                abort(400, "Missing name")
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=["PUT"])
def city_update(city_id=None):
    """Updates a city from a dict"""

    cities_dict = storage.all(City)

    my_city_obj = storage.get(City, city_id)

    if my_city_obj is not None:
        update_dict = request.get_json(silent=True)
        if update_dict is not None:
            for key, value in update_dict.items():
                setattr(my_city_obj, key, value)
                my_city_obj.save()
            return make_response(jsonify(my_city_obj.to_dict()), 200)
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
