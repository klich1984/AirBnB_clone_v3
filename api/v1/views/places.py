"""REST full view for cities objects"""
from flask import Flask, abort, jsonify, make_response
from flask import request
from api.v1.views import app_views
from models.city import City
from models.place import Place
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
