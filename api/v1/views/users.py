#!/usr/bin/python3
"""Config endpoint for REST resource user"""
from flask import Flask, abort, jsonify, make_response
from flask import request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=["POST", "GET"])
@app_views.route('/users/<user_id>', methods=('DELETE', 'PUT', "GET"))
def user_get_id(user_id=None):
    """Retrieves a user object by its id"""

    user_dict = storage.all(User)
    obj_list = []

    if user_id is not None:
        my_user_obj = storage.get(User, user_id)

        if my_user_obj is not None:
            if request.method == 'DELETE':
                storage.delete(my_user_obj)
                return make_response(jsonify({}), 200)

            if request.method == 'GET':
                return jsonify(my_user_obj.to_dict())

            if request.method == 'PUT':
                update_dict = request.get_json(silent=True)
                if update_dict is not None:
                    for key, value in update_dict.items():
                        setattr(my_user_obj, key, value)
                        my_user_obj.save()
                    return make_response(jsonify(my_user_obj.to_dict()),
                                         200)
                else:
                    abort(400, "Not a JSON")
        else:
            abort(404)
    else:
        # In case user_id is None
        if request.method == 'POST':
            my_json = request.get_json(silent=True)
            if my_json is not None:
                if "email" in my_json:
                    if "password" in my_json:
                        email = my_json["email"]
                        password = my_json["password"]
                        new_user = User(email=email, password=password)
                        new_user.save()
                        return make_response(jsonify(new_user.to_dict()), 201)
                    else:
                        abort(400, "Missing password")
                else:
                    abort(400, "Missing email")
            else:
                # print("funcionó el none!")
                abort(400, "Not a JSON")

        for value in user_dict.values():
            obj_list.append(value.to_dict())
        return jsonify(obj_list)
