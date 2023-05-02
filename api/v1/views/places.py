#!/usr/bin/python3
"""
Same as State, create a new view for City
objects that handles all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def place1(city_id):
    slist = []
    states = storage.all(City)
    key = "City."+city_id
    if key not in states:
        abort(404)
    city = storage.all(Place).values()
    for stat in city:
        pp = stat.to_dict()
        if "city_id" in pp:
            if pp["city_id"] == city_id:
                slist.append(stat.to_dict())
    return jsonify(slist)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place2(place_id):
    """Retrieves a city object"""
    city = storage.all(Place)
    key = "Place."+place_id
    if key not in city:
        abort(404)
    a = city[key]
    return jsonify(a.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def place3(place_id):
    city = storage.all(Place)
    key = "Place."+place_id
    if key not in city:
        abort(404)
    a = city[key]
    storage.delete(a)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def place4(city_id):
    states = storage.all(City)
    key = "City."+city_id
    if key not in states:
        abort(404)
    js = request.get_json()
    if not js:
        abort(400, 'Not a JSON')
    if 'user_id' not in js:
        abort(400, 'Missing user_id')
    if 'name' not in js:
        abort(400, 'Missing name')
    user = storage.all(User)
    key = "User."+js['user_id']
    if key not in user:
        abort(404)
    city = Place(**js)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def place5(place_id):
    city = storage.all(Place)
    key = "Place."+place_id
    if key not in city:
        abort(404)
    js = request.get_json()
    if not js:
        abort(400, 'Not a JSON')
    a = city[key]
    m = a.__dict__
    for i in js:
        if i not in ["id", "created_at",
                     "updated_at"]:
            m[i] = js[i]
    storage.save()
    return jsonify(m.to_dict()), 200
