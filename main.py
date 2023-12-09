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
from dutchx import create_order, fetch_all_orders

app = Flask(__name__)

# Create Compress with default params
compress = Compress()
# Init compress for our Flask app
compress.init_app(app)


@app.route('/')
def hello_world():
    return render_template('index.html')


struct UserOrder {
    address from;
    uint256 fromChainId;
    address fromToken;
    uint256 fromAmount;
    uint256 toChainId;
    address toToken;
    uint256 startingPrice;
    uint256 endingPrice;
    uint256 stakeAmount;
    uint256 creationTimestamp;
    uint256 duration;
    uint256 nonce;
}


@app.route('/create', methods=["POST"])
def create():
    order = request.json["order"]
    signature = request.json["signature"]
    orderid = request.json["orderid"]
    api_key = request.headers["api_key"]
    if api_key != os.environ['api_key']:
        return {"error": {"code": 403, "message": "Auth Failed"}}
    order_status = create_order(order, signature, orderid)
    if order_status:
        return {"status": "order_created", "code": 200}
    else:
        return {"status": "order_exists", "code": 200}

@app.route('/fetch', methods=["POST"])
def fetch_orders():
    api_key = request.headers["api_key"]
    if api_key != os.environ['api_key']:
        return {"error": {"code": 403, "message": "Auth Failed"}}
    all_orders = fetch_all_orders()
    return {"orders": all_orders, "status": "success", "code": 200}

@app.route('/claim_order', methods=["POST"])
def fetch_orders():
    api_key = request.headers["api_key"]
    if api_key != os.environ['api_key']:
        return {"error": {"code": 403, "message": "Auth Failed"}}
    all_orders = fetch_all_orders()
    return {"orders": all_orders, "status": "success", "code": 200}


@app.route('/get')
def get_txns():
    print_row()
    return "0xFUckYea"


if __name__ == '__main__':
    # Create WSGI server with params for Repl.it (IP 0.0.0.0, port 8080)
    # for our Flask app
    http_server = WSGIServer(('0.0.0.0', 8080), app)
    # Start WSGI server
    http_server.serve_forever()
