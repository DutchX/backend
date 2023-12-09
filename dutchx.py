# from replit import db

import json

# Specify the file path where you want to save the JSON data
file_path = "data.json"


def create_order(order, signature, orderid):

    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    keys = data.keys()

    if orderid in keys:
        return False
    data[orderid] = {"order": order, "signature": signature, "status": "open"}

    with open(file_path, "w") as json_file:
        json.dump(data, json_file)
    return True


def claim_order(orderid):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    keys = data.keys()
    if orderid not in keys:
        return False
    order = data[orderid]
    if data[orderid]["status"] != "open":
        return "Already claimed/filled"
    data[orderid]["status"] = "claimed"

    with open(file_path, "w") as json_file:
        json.dump(data, json_file)

    return "Claimed"


def fetch_all_orders():
    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    keys = data.keys()
    all_orders = []
    for key in keys:
        if data[key]["status"] != "open":
            continue
        data[key]["orderId"] = key
        all_orders.append(data[key])
    return all_orders


def order_status(order_id):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    return data[order_id]
