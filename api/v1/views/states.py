#!/usr/bin/python3
"""
Create a new view for State objects that handles
all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
import models


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def status():
    """
    A simple endpoint to greet a user by their name.
    ---
    parameters:
      - name: states
        in: path
        type: string
        enum: ["state"]
        required: true
        default: /
    definitions:
      Hello:
        type: string
        properties:
          hello: array
    responses:
      200:
        description: A list of colors (may be filtered by palette)
        schema:
          $ref: '#/definitions/Hello'
        examples:
          hello mayouka
    """
    slist = []
    states = storage.all(State).values()
    for state in states:
        slist.append(state.to_dict())
    return jsonify(slist)


@app_views.route('/states/<state_id>/', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    A simple endpoint to greet a user by their name.
    ---
    parameters:
      - name: state get
        in: path
        type: string
        enum: ["0d054d4d-c448-4639-bd25-f710cc235864"]
        required: true
        default: /states/<state_id>
    definitions:
      state:
        type: string
        properties:
          states: states id
    responses:
      200:
        description: states/state_id
        schema:
          $ref: '#/definitions/state'
        examples:
          hello mayouka
    """
    states = storage.all(State)
    key = "State."+state_id
    if key not in states:
        abort(404)
    a = states[key]
    return jsonify(a.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    A simple endpoint to greet a user by their name.
    ---
    parameters:
      - name: Delete
        in: path
        type: string
        enum: ["88bc6f3c-c535-4b80-93dc-b1cd4e2d61a5"]
        required: true
        default: /states/<state_id>
    definitions:
      DELETE:
        type: string
        properties:
          delete: delete file
    responses:
      200:
        description: delete id
        schema:
          $ref: '#/definitions/DELETE'
        examples:
          DELETE /api/v1/states/<state_id>
    """
    states = storage.all(State)
    key = "State."+state_id
    if key not in states:
        abort(404)
    a = states[key]
    storage.delete(a)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post():
    """
    A simple endpoint to greet a user by their name.
    ---
    parameters:
      - name: Delete
        in: path
        type: string
        enum: ["states"]
        required: true
        default: /states/<state_id>
    definitions:
      DELETE:
        type: string
        properties:
          delete: delete file
    responses:
      200:
        description: delete id
        schema:
          $ref: '#/definitions/DELETE'
        examples:
          DELETE /api/v1/states/<state_id>
    """
    js = request.get_json()
    if not js:
        abort(400, 'Not a JSON')
    if 'name' not in js:
        abort(400, 'Missing name')
    state = State(**js)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put(state_id):
    js = request.get_json()
    states = storage.all(State)
    key = "State."+state_id
    if key not in states:
        abort(404)
    if not js:
        abort(400, 'Not a JSON')
    a = states[key]
    m = a.__dict__
    for i in js:
        if i not in ["id", "created_at",
                     "updated_at"]:
            m[i] = js[i]
            storage.save()
    storage.save()
    return jsonify(a.to_dict()), 200
