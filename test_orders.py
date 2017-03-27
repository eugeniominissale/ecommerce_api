from app import app
from models import  Order, OrderItem, Item, database, create_tables
from http.client import CREATED, NO_CONTENT, NOT_FOUND, OK, INTERNAL_SERVER_ERROR
from peewee import SqliteDatabase
import json
import uuid
import datetime
import sys
sys.path.append('./views')

class TestOrders:
	@classmethod
	def setup_class(cls):
		test_db = SqliteDatabase(':memory:')
		Order._meta.database = test_db
		Item._meta.database = test_db
		OrderItem._meta.database = test_db
		test_db.connect()
		Order.create_table(fail_silently=False)
		Item.create_table(fail_silently=False)
		OrderItem.create_table(fail_silently=False)
		cls.app = app.test_client()

	def setup_method(self):
		Order.delete().execute()
		Item.delete().execute()
		OrderItem.delete().execute()

	def test_get_orders__empty(self):
		resp = self.app.get('/orders/')
		assert resp.status_code == OK
		assert json.loads(resp.data) == []

	def test_get_orders(self):
		item1 = Item.create(
			name = "item1",
			picture = uuid.uuid4(),
			price = "20.00",
			description = "item1description."
		)
		order_id =  uuid.uuid4()
		dt = datetime.datetime.now().isoformat()
		order1 = Order.create(
			order_id = order_id,
			date = dt,
			total_price = 100,
			delivery_address = 'Via Rossi 12'
		)
		orderitem1 = OrderItem.create(
			order = order1,
			item = item1,
			quantity = 2,
			subtotal = 50.00
		)
		resp = self.app.get('/orders/')
		assert resp.status_code == OK
		assert json.loads(resp.data) == [{"order_id": str(order_id), "date": dt, "total_price": 100.0, "delivery_address": 'Via Rossi 12', "items": [{"quantity": 2, "subtotal": 50.0, "item_name": "item1", "item_description": "item1description."}]}]

	def test_get_order__non_existing_empty_orders(self):
		resp = self.app.get('/orders/{}©√'.format(uuid.uuid4()))
		assert resp.status_code == NOT_FOUND

	def test_get_order__non_existing(self):
		item1 = Item.create(
			name = "item1",
			picture = uuid.uuid4(),
			price = "20.00",
			description = "item1description."
		)
		order1 = Order.create(
			order_id = uuid.uuid4(),
			date = datetime.datetime.now().isoformat(),
			total_price = 100,
			delivery_address = 'Via Rossi 12'
		)
		orderitem1 = OrderItem.create(
			order = order1,
			item = item1,
			quantity = 2,
			subtotal = 40.00
		)
		resp = self.app.get('/orders/{}©√'.format(uuid.uuid4()))
		assert resp.status_code == NOT_FOUND

	def test_get_order(self):
		item1 = Item.create(
			name = "item1",
			picture = uuid.uuid4(),
			price = "20.00",
			description = "item1description."
		)

		order_id = uuid.uuid4()
		dt = datetime.datetime.now().isoformat()
		order1 = Order.create(
			order_id = order_id,
			date = dt,
			total_price = 100,
			delivery_address = 'Via Rossi 12'
		)
		orderitem1 = OrderItem.create(
			order = order1,
			item = item1,
			quantity = 2,
			subtotal = 50.00
		)
		item2 = Item.create(
			name = "item2",
			picture = uuid.uuid4(),
			price = "20.00",
			description = "item2description."
		)
		order2 = Order.create(
			order_id = uuid.uuid4(),
			date = datetime.datetime.now().isoformat(),
			total_price = 200,
			delivery_address = 'Via Verdi 12'
		)
		orderitem1 = OrderItem.create(
			order = order2,
			item = item2,
			quantity = 3,
			subtotal = 100.00
		)

		resp = self.app.get('/orders/{}'.format(order_id))
		assert resp.status_code == OK
		assert json.loads(resp.data) == [str(order_id), dt, 100.0, 'Via Rossi 12', [{"quantity": 2, "subtotal": 50.0, "item_name": "item1", "item_description": "item1description."}]]

	def test_delete_article__success(self):
		item1 = Item.create(
			name = "item1",
			picture = uuid.uuid4(),
			price = "20.00",
			description = "item1description."
		)
		order_id =  uuid.uuid4()
		dt = datetime.datetime.now().isoformat()
		order1 = Order.create(
			order_id = order_id,
			date = dt,
			total_price = 100,
			delivery_address = 'Via Rossi 12'
		)
		orderitem1 = OrderItem.create(
			order = order1,
			item = item1,
			quantity = 2,
			subtotal = 50.00
		)
		order2 = Order.create(
			order_id = uuid.uuid4(),
			date = datetime.datetime.now().isoformat(),
			total_price = 200,
			delivery_address = 'Via Verdi 12'
		)
		resp = self.app.delete('/orders/{}'.format(str(order_id)))
		assert resp.status_code == NO_CONTENT
		assert len(Order.select()) == 1
		assert len(OrderItem.select()) == 0
		assert Order.get(order_id = order2.order_id)

	def test_delete_order__failure_non_existing_empty_orders(self):
		resp = self.app.delete('/orders/{}'.format(str(uuid.uuid4())))
		assert resp.status_code == NOT_FOUND

	def test_delete_order__failure__failure_non_existing(self):
		order1 = Order.create(
			order_id = uuid.uuid4(),
			date = datetime.datetime.now().isoformat(),
			total_price = 100,
			delivery_address = 'Via Rossi 12'
		)
		resp = self.app.delete('/orders/{}'.format(str(uuid.uuid4())))		
		assert resp.status_code == NOT_FOUND
		assert len(Order.select()) == 1
