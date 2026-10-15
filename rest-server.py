#!/usr/bin/env python3

import base64
from flask import Flask, request, Response
import jsonpickle
from PIL import Image
import io
import argparse

# Initialize the Flask application
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)


@app.route('/api/add/<int:a>/<int:b>', methods=['GET', 'POST'])
def add(a, b):
    response = {'sum': str(a + b)}
    response_pickled = jsonpickle.encode(response)
    return Response(
        response=response_pickled,
        status=200,
        mimetype="application/json"
    )


@app.route('/api/rawimage', methods=['POST'])
def rawimage():
    r = request

    # Convert the data to a PIL image type so we can extract dimensions
    try:
        ioBuffer = io.BytesIO(r.data)
        img = Image.open(ioBuffer)

        response = {
            'width': img.size[0],
            'height': img.size[1]
        }
    except:
        response = {'width': 0, 'height': 0}

    response_pickled = jsonpickle.encode(response)
    return Response(
        response=response_pickled,
        status=200,
        mimetype="application/json"
    )


@app.route('/api/dotproduct', methods=['POST'])
def dotproduct():
    r = request 
    # try to do the dotproduct 
    try: 
        lists = r.get_json()
        a = lists['a']
        b = lists['b']
        if(len(a) != len(b)):
            raise Exception("A and B input to dotproduct are not of same size")
        c = sum([item_a * item_b for (item_a, item_b) in zip(a,b)])
        response = {
            'dotproduct': c
        }
    except Exception as e: # 400 means bad input, we're just gonna assume it's their fault tehee 
        return Response(jsonpickle.encode({'error': str(e)}), status=400, mimetype="application/json")
    response_pickled = jsonpickle.encode(response)
    return Response(
        response=response_pickled,
        status=200,
        mimetype="application/json"
    )


@app.route('/api/jsonimage', methods=['POST'])
def jsonimage():
    r = request

    # Convert the data to a PIL image type so we can extract dimensions
    try:
        img_bytes = base64.b64decode(r.get_json()['image'])
        img = Image.open(io.BytesIO(img_bytes))

        response = {
            'width': img.size[0],
            'height': img.size[1]
        }
    except:
        response = {'width': 0, 'height': 0}

    response_pickled = jsonpickle.encode(response)
    return Response(
        response=response_pickled,
        status=200,
        mimetype="application/json"
    )


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Flask REST server'
    )

    parser.add_argument(
        '-p', '--port',
        type=int,
        default=5000,
        help='Port on which to run the server (default: 5000)'
    )

    args = parser.parse_args()

    # Start Flask app
    app.run(host='0.0.0.0', port=args.port)
