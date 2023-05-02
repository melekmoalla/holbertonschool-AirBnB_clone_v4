#!/usr/bin/python3
"""
Same as State, create a new view for City
objects that handles all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def review1(place_id):
    slist = []
    states = storage.all(Place)
    key = "Place."+place_id
    if key not in states:
        abort(404)
    city = storage.all(Review).values()
    for stat in city:
        pp = stat.to_dict()
        if "place_id" in pp:
            if pp["place_id"] == place_id:
                slist.append(stat.to_dict())
    return jsonify(slist)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review2(review_id):
    """Retrieves a city object"""
    city = storage.all(Review)
    key = "Review."+review_id
    if key not in city:
        abort(404)
    a = city[key]
    return jsonify(a.to_dict())


@app_views.route("/reviews/<review_id>",
                 methods=['DELETE'], strict_slashes=False)
def review3(review_id):
    city = storage.all(Review)
    key = "Review."+review_id
    if key not in city:
        abort(404)
    a = city[key]
    storage.delete(a)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def review4(place_id):
    states = storage.all(Place)
    me = "Place."+place_id
    if me not in states:
        abort(404)
    js = request.get_json()
    if not js:
        abort(400, 'Not a JSON')
    if 'user_id' not in js:
        abort(400, 'Missing user_id')
    if 'text' not in js:
        abort(400, 'Missing text')
    user = storage.all(User)
    key = "User."+js['user_id']
    if key not in user:
        abort(404)
    city = Review(**js)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def review5(review_id):
    city = storage.all(Review)
    key = "Review."+review_id
    if key not in city:
        abort(404)
    js = request.get_json()
    if not js:
        abort(400, 'Not a JSON')
    a = city[key]
    m = a.__dict__
    for i in js:
        if i not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            m[i] = js[i]
    storage.save()
    return jsonify(m.to_dict()), 200
