#!/usr/bin/python3
"""
Same as State, create a new view for City
objects that handles all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities(state_id):
    slist = []
    states = storage.all(State)
    key = "State."+state_id
    if key not in states:
        abort(404)
    city = storage.all(City).values()
    for stat in city:
        pp = stat.to_dict()
        if "state_id" in pp:
            if pp["state_id"] == state_id:
                slist.append(stat.to_dict())
    return jsonify(slist)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get1(city_id):
    """Retrieves a city object"""
    city = storage.all(City)
    key = "City."+city_id
    if key not in city:
        abort(404)
    a = city[key]
    return jsonify(a.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete2(city_id):
    city = storage.all(City)
    key = "City."+city_id
    if key not in city:
        abort(404)
    a = city[key]
    storage.delete(a)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post3(state_id):
    states = storage.all(State)
    key = "State."+state_id
    if key not in states:
        abort(404)
    js = request.get_json()
    if not js:
        abort(400, 'Not a JSON')
    if 'name' not in js:
        abort(400, 'Missing name')
    city = City(**js)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put4(city_id):
    city = storage.all(City)
    key = "City."+city_id
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
