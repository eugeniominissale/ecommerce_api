from flask import Flask
from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource
from http.client import CREATED
from http.client import NO_CONTENT
from http.client import NOT_FOUND
from http.client import OK
from http.client import INTERNAL_SERVER_ERROR
import uuid
import datetime
from flask import request

from models import Order, OrderItem, Item, database, populate_tables1

app = Flask(__name__)
api = Api(app)

@app.before_request
def _db_connect():
	if database.is_closed():
		database.connect()

@app.teardown_request
def _db_close(exc):
	if not database.is_closed():
		database.close()

def non_emtpy_dict(val, name):
	if not dict(val).strip():
		raise ValueError('The argument {} is not empty'.format(name))
	return str(val)

#populate_tables()

class OrdersHandler(Resource):
	def get(self):
		orders = {}

		res = (Order
		 	.select(Order, OrderItem, Item)
		 	.join(OrderItem)
		 	.join(Item))

		for row in res:
			if row.order_id not in orders:
				orders[row.order_id] = {
					'order_id': str(row.order_id),
					'date': row.date,
					'total_price': row.total_price,
					'delivery_address': row.delivery_address,
					'items': []
				}
			orders[row.order_id]['items'].append({
				'quantity': row.orderitem.quantity,
				'subtotal': row.orderitem.subtotal,
				'item_name': row.orderitem.item.name,
				'item_description': row.orderitem.item.description,
			})
			
		return list(orders.values()), OK
		
	def post(self):	
		res = validateRequest('order')

def validateRequest(arg):
	return request.form[arg]

# Views
		
api.add_resource(OrdersHandler, '/orders/')



