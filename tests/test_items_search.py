from models import Item, ItemIndex
from tests.test_utils import open_with_auth, add_user, add_address
from tests.test_case import TestCase
from http.client import (OK, NOT_FOUND, NO_CONTENT, BAD_REQUEST,
                         CREATED, CONFLICT, UNAUTHORIZED)
import json
import uuid

ITEM1 = {
    'item_id': '429994bf-784e-47cc-a823-e0c394b823e8',
    'name': 'mario',
    'price': 20.20,
    'description': 'svariati mariii',
    'availability': 1,
}

ITEM2 = {
    'item_id': '577ad826-a79d-41e9-a5b2-7955bcf03499',
    'name': 'GINO',
    'price': 30.20,
    'description': 'svariati GINIIIII',
    'availability': 2,
}


class TestItemsSearch(TestCase):

    def test_get_items_search__success(self):
        item1 = Item.create(**ITEM1)
        item2 = Item.create(**ITEM2)

        ItemIndex.create(
            item_id=item1.item_id,
            name=item1.name,
            description=item1.description)
        ItemIndex.create(
            item_id=item2.item_id,
            name=item2.name,
            description=item2.description)

        query = "mario"
        resp = self.app.get('/items/db', data=query)
