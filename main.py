# -*- coding: utf-8 -*-
# Import Monkey module from gevent for monkey-patching

from flask import Flask, render_template, request
from flask_compress import Compress
from gevent import monkey
from gevent.pywsgi import WSGIServer
import os
# Monkey-patching standart Python library for async working
monkey.patch_all()
# Import WSGI server from Gevent
# Import Compress module from Flask-Compress for compress static
# content (HTML, CSS, JS)
# from database import insert_row, print_row
from dutchx import create_order, fetch_all_orders, claim_order

app = Flask(__name__)

# Create Compress with default params
compress = Compress()
# Init compress for our Flask app
compress.init_app(app)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/create_order', methods=["POST"])
def create():
    order = request.json["order"]
    signature = request.json["signature"]
    orderid = request.json["orderId"]
    api_key = request.headers["x-api-key"]
    if api_key != os.environ['api_key']:
        return {"error": {"code": 403, "message": "Auth Failed"}}
    order_status = create_order(order, signature, orderid)
    if order_status:
        return {"status": "order_created", "code": 200}
    else:
        return {"status": "order_exists", "code": 200}


@app.route('/fetch_orders', methods=["GET"])
def fetch_orders():
    # api_key = request.headers["api_key"]
    # if api_key != os.environ['api_key']:
    #     return {"error": {"code": 403, "message": "Auth Failed"}}
    all_orders = fetch_all_orders()
    return {"orders": all_orders, "code": 200}


@app.route('/claim_order', methods=["POST"])
def claim():
    orderid = request.json["orderId"]
    api_key = request.headers["x-api-key"]
    if api_key != os.environ['api_key']:
        return {"error": {"code": 403, "message": "Auth Failed"}}

    all_orders = claim_order(orderid)
    return {"orders": all_orders, "code": 200}


if __name__ == '__main__':
    # Create WSGI server with params for Repl.it (IP 0.0.0.0, port 8080)
    # for our Flask app
    http_server = WSGIServer(('0.0.0.0', 8080), app)
    # Start WSGI server
    http_server.serve_forever()
