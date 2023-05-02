#!/usr/bin/python3
"""
Create a new view for User object that
handles all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.user import User
import models


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users1():
    slist = []
    states = storage.all(User).values()
    for state in states:
        slist.append(state.to_dict())
    return jsonify(slist)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def users2(user_id):
    """Retrieves a State object"""
    states = storage.all(User)
    key = "User."+user_id
    if key not in states:
        abort(404)
    a = states[key]
    return jsonify(a.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def users3(user_id):
    states = storage.all(User)
    key = "User."+user_id
    if key not in states:
        abort(404)
    a = states[key]
    storage.delete(a)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def users4():
    js = request.get_json()
    if not js:
        abort(400, 'Not a JSON')
    if 'email' not in js:
        abort(400, 'Missing email')
    if 'password' not in js:
        abort(400, 'Missing password')
    state = User(**js)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def users5(user_id):
    states = storage.all(User)
    key = "User."+user_id
    if key not in states:
        abort(404)
    js = request.get_json()
    if not js:
        abort(400, 'Not a JSON')
    a = states[key]
    m = a.__dict__
    for i in js:
        if i not in ["id", "created_at",
                     "updated_at", "email"]:
            m[i] = js[i]
    storage.save()
    return jsonify(m.to_dict()), 200
