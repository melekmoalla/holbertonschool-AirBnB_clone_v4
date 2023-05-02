#!/usr/bin/python3
"""
create a variable app, instance of Flask
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os
from flasgger import Swagger

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)

swagger = Swagger(app)


@app.route("/")
def hello():
    """
    A simple endpoint to greet a user by their name.
    ---
    parameters:
      - name: palette
        in: path
        type: string
        enum: ["hello"]
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
    return jsonify("hello mayouka")


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


"""
create a handler for 404 errors that
returns a JSON-formatted 404 status code
response
"""


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", 5000)
    app.run(debug=True, host=host, port=port, threaded=True)
