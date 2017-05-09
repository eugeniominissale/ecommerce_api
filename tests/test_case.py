"""
Test case for setup and teardown methods
"""

from app import app
from models import Address, Item, ItemIndex, Order, OrderItem, Picture, User
from playhouse.sqlite_ext import SqliteExtDatabase

TABLES = [Address, Item, ItemIndex, Order, OrderItem, Picture, User]


class TestCase:
    """
    Created TestCase to avoid duplicated code in the other tests
    """
    TEST_DB = SqliteExtDatabase(':memory:')

    @classmethod
    def setup_class(cls):
        for table in TABLES:
            table._meta.database = cls.TEST_DB
            table.create_table(fail_silently=True)
        cls.app = app.test_client()

    def setup_method(self):
        for table in TABLES:
            table.delete().execute()
