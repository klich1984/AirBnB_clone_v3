#!/usr/bin/python3
"""REST full view for places_reviews objects"""
from flask import Flask, abort, jsonify, make_response
from flask import request
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def place_review_from_place(place_id=None):
    """Retrieves all places from a cities"""
    my_p_review_obj = storage.get(Place, place_id)

    if my_p_review_obj is not None:
        review_dict = storage.all(Review)
        review_list = []
        for class_id, class_dict in review_dict.items():
            if place_id == class_dict.place_id:
                review_obj = storage.get(Review, class_dict.id)
                review_list.append(review_obj.to_dict())
        return (jsonify(review_list))
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=["GET", "DELETE"])
def review_get_id(review_id=None):
    """Retrieves a review by its id"""
    review_obj = storage.get(Review, review_id)

    if review_obj is not None:
        if request.method == "GET":
            return jsonify(review_obj.to_dict())

        elif request.method == "DELETE":
            storage.delete(review_obj)
            return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def reviews_create(place_id=None):
    """Creates a places within a cities by its id"""
    my_place_obj = storage.get(Place, place_id)

    if my_place_obj is not None:
        # json that request curl
        my_json = request.get_json(silent=True)
        if my_json is not None:
            if "user_id" in my_json:
                my_user_obj = storage.get(User, my_json['user_id'])
                if my_user_obj is not None:
                    if "text" in my_json:
                        text = my_json["text"]
                        new_r = Review(text=text, user_id=my_json['user_id'],
                                       place_id=place_id)
                        new_r.save()
                        return make_response(jsonify(new_r.to_dict()), 201)
                    else:
                        abort(400, "Missing text")
                else:
                    abort(404)
            else:
                abort(400, "Missing user_id")
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def reviews_update(review_id=None):
    """Updates a reviews from a dict"""
    my_review_obj = storage.get(Review, review_id)

    if my_review_obj is not None:
        update_dict = request.get_json(silent=True)
        if update_dict is not None:
            for key, value in update_dict.items():
                setattr(my_review_obj, key, value)
                my_review_obj.save()
            return make_response(jsonify(my_review_obj.to_dict()), 200)
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
