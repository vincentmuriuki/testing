from flask import Flask, request, abort, jsonify, make_response
import markdown
import json
import datetime
import os

app = Flask(__name__)

with open('orders.json') as orders_json:
    orders = json.load(orders_json)

@app.route('/')
def index():
    """ Provide the documentation to the landing page """
    return "<h1> Fast Food Fast Api</h1> <p>Use this url to test api endpoints on postman</p>"

@app.route('/api/v1/orders/', methods=['GET'])
def get_orders():
    if len(orders) == 0:
        # if no orders return no orders 
        return jsonify({"message":"No orders"}), 200
    else:
        return jsonify(
            {
                "message":"Success",
                "orders":orders
            }
        ), 200

@app.route('/api/v1/orders/<int:identifier>/', methods=['GET'])
def get_specific_order(identifier):

    # get an order with the same identifier 
    order = [order for order in orders if order['id'] == identifier]

    if len(order) == 0:

        # return a resource not found if no order existing
        abort(404)

    # return the order with the same identifier
    return jsonify(
        {
            "message":"Success",
            "order":order
        }
    ), 200

@app.route('/api/v1/orders/', methods=['POST'])
def place_an_order():

    request_data = request.get_json()

    # new order dictionary to be added to the rest of the orders
    new_order = {
        'id':len(orders) + 1,
        'user_name':request_data['user_name'],
        'products':{
            "name":request_data['products']['name'],
            "qty":request_data['products']['qty'],
            "price":request_data['products']['price']
        },
        'status':False,
        'ordered_date': str(datetime.datetime.now()),
        'delivered_date':None
    }

    # add the dictionary to orders
    orders.append(new_order)

    # return status 201 if successfull
    return jsonify(
        {
            "message":"Order Placed",
            "order":new_order
        }
    ), 201

@app.route('/api/v1/orders/<int:identifier>/', methods=['PUT'])
def update_order_status(identifier):
    request_data = request.get_json()

    # get the specific order of that identifier
    order = [order for order in orders if order['id'] == identifier]

    # validation if the order object lacks any of the conditions
    if len(order) == 0:
        abort(404)
    if (not request_data or 
            ('id' in request_data and type(request_data['id']) is not int) or
            ('user_name' in request_data and type(request_data['user_name']) != str) or
            ('products' in request_data and type(request_data['products']) is not str) or
            ('status' in request_data and type(request_data['status']) is not bool) or 
            ('ordered_date' in request_data and type(request_data['ordered_date']) is not str)):

        abort(400)

    # update the status of the order and the delivered date
    order[0]['status'] = request_data.get('status', order[0]['status'])
    order[0]['delivered_date'] = str(datetime.datetime.now())
    return jsonify({'order': order[0]}), 202

@app.route('/api/v1/orders/<int:identifier>/', methods=['DELETE'])
def delete_an_order(identifier):

    # get the specific order to delete
    order = [order for order in orders if order['id'] == identifier]

    # if the order is nothing return a status not found
    if len(order) == 0:
        abort(404)

    # use the remove() method to remove the specific order
    orders.remove(order[0])

    # return a status 204 if successfull
    return jsonify({'result': True}), 204


if __name__ == "__main__":
    app.run(debug=True)