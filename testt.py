#!/usr/bin/python3

from flask import Flask, jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
import models


def put(state_id,  js):

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
    return a


a= put("bd688c87-bc2a-4666-997c-fe93f72c0c7d", {"pp": 'mayouka'})
print(a)