from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os

app = Flask(__name__)
# Path for the running application. Put db here.
basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/super_simple')
def super_simple():
    return jsonify(message='Oba. Lá vem ela.')

@app.route('/not_found')
def not_found():
    return jsonify(message="That resource was not found"), 404

@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message=f"Sorry {name}, you are not old enough."), 401
    else:
        return jsonify(message=f"Welcome {name}!")

@app.route('/url_variables/<string:name>/<int:age>') #flask function, so string is string rather than the python str
def url_variables(name: str, age: int):
    # uses variable rule matching to grab variables from url, rather than defining variables within the function
    if age < 18:
        return jsonify(message=f"Sorry {name}, you are not old enough."), 401
    else:
        return jsonify(message=f"Welcome {name}!")


if __name__ == '__main__':
    app.run(debug=True)
