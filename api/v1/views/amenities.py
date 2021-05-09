#!/usr/bin/python3
"""Config endpoint for REST resource amenities"""
from flask import Flask, abort, jsonify, make_response
from flask import request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=["POST", "GET"])
@app_views.route('/amenities/<amenity_id>', methods=('DELETE', 'PUT', "GET"))
def amenities_get_id(amenity_id=None):
    """Retrieves a amenities object by its id"""

    amenity_dict = storage.all(Amenity)
    obj_list = []

    if amenity_id is not None:
        my_amenities_obj = storage.get(Amenity, amenity_id)

        if my_amenities_obj is not None:
            if request.method == 'DELETE':
                storage.delete(my_amenities_obj)
                return make_response(jsonify({}), 200)

            if request.method == 'GET':
                return jsonify(my_amenities_obj.to_dict())

            if request.method == 'PUT':
                update_dict = request.get_json(silent=True)
                if update_dict is not None:
                    for key, value in update_dict.items():
                        setattr(my_amenities_obj, key, value)
                        my_amenities_obj.save()
                    return make_response(jsonify(my_amenities_obj.to_dict()),
                                         200)
                else:
                    abort(400, "Not a JSON")
        else:
            abort(404)
    else:
        # In case amenity_id is None
        if request.method == 'POST':
            my_json = request.get_json(silent=True)
            if my_json is not None:
                if "name" in my_json:
                    name = my_json["name"]
                    new_amenities = Amenity(name=name)
                    new_amenities.save()
                    return make_response(jsonify(new_amenities.to_dict()), 201)
                else:
                    abort(400, "Missing name")
            else:
                # print("funcionó el none!")
                abort(400, "Not a JSON")

        for value in amenity_dict.values():
            obj_list.append(value.to_dict())
        return jsonify(obj_list)
