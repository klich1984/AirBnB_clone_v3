#!/usr/bin/python3
"""REST full view for places objects"""
from flask import Flask, abort, jsonify, make_response
from flask import request
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def place_from_cities(city_id=None):
    """Retrieves all places from a cities"""

    # states_dict = storage.all(State)
    places_dict = storage.all(Place)
    places_list = []

    my_city_obj = storage.get(City, city_id)

    if my_city_obj is not None:
        for class_id, class_dict in places_dict.items():
            if city_id == class_dict.city_id:
                city_obj = storage.get(Place, class_dict.id)
                places_list.append(city_obj.to_dict())
        return (jsonify(places_list))
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=["GET", "DELETE"])
def place_get_id(place_id=None):
    """Retrieves a place by its id"""

    places_dict = storage.all(Place)

    for p_id, place_objs in places_dict.items():
        if place_id == place_objs.id:
            if request.method == "GET":
                return jsonify(place_objs.to_dict())

            elif request.method == "DELETE":
                storage.delete(place_objs)
                return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def place_create(city_id=None):
    """Creates a places within a cities by its id"""

    # states_dict = storage.all(State)
    # places_dict = storage.all(Place)
    # cities_list = []

    my_cities_obj = storage.get(City, city_id)

    if my_cities_obj is not None:
        my_json = request.get_json(silent=True)
        if my_json is not None:
            if "user_id" in my_json:
                my_user_obj = storage.get(User, my_json['user_id'])
                if my_user_obj is not None:
                    if "name" in my_json:
                        name = my_json["name"]
                        new_p = Place(name=name, user_id=my_json['city_id'],
                                      city_id=city_id)
                new_p.save()
                return make_response(jsonify(new_p.to_dict()), 201)
            else:
                abort(400, "Missing name")
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)

@app_views.route("/places/<place_id>", methods=["PUT"])
def place_update(place_id=None):
    """Updates a places from a dict"""
    my_place_obj = storage.get(Place, place_id)

    if my_place_obj is not None:
        update_dict = request.get_json(silent=True)
        if update_dict is not None:
            for key, value in update_dict.items():
                setattr(my_place_obj, key, value)
                my_place_obj.save()
            return make_response(jsonify(my_place_obj.to_dict()), 200)
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
