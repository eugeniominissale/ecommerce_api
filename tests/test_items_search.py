from models import Item, ItemIndex
from tests.test_case import TestCase
from http.client import OK, BAD_REQUEST, NOT_FOUND
import json

ITEM1 = {
    'uuid': '429994bf-784e-47cc-a823-e0c394b823e8',
    'name': 'mario',
    'price': 20.20,
    'description': 'svariati mariii',
    'availability': 1,
}

ITEM2 = {
    'uuid': '577ad826-a79d-41e9-a5b2-7955bcf03499',
    'name': 'GINO',
    'price': 30.20,
    'description': 'svariati GINIIIII',
    'availability': 2,
}

ITEM3 = {
    'uuid': 'f47f87c6-0de0-4dbf-9aae-841f7cdea11d',
    'name': 'GIOVANNI',
    'price': 10.20,
    'description': 'svariati GIOVANNI',
    'availability': 3,
}


class TestItemsSearch(TestCase):

    def test_get_items_search__failed(self):
        item1 = Item.create(**ITEM1)

        ItemIndex.create(
            uuid=item1.uuid,
            name=item1.name,
            description=item1.description)

        query = ""
        resp = self.app.get('/items/db', query_string=query)
        items = json.loads(resp.data)

        assert resp.status_code == BAD_REQUEST
        assert items is None

    def test_get_items_search__not_found(self):
        item1 = Item.create(**ITEM1)

        ItemIndex.create(
            uuid=item1.uuid,
            name=item1.name,
            description=item1.description)

        query = "GIOVANNI"
        resp = self.app.get('/items/db', query_string=query)
        items = json.loads(resp.data)

        assert resp.status_code == NOT_FOUND
        assert items is None

    def test_get_items_search__success(self):
        item1 = Item.create(**ITEM1)
        item2 = Item.create(**ITEM2)
        item3 = Item.create(**ITEM3)

        ItemIndex.create(
            uuid=item1.uuid,
            name=item1.name,
            description=item1.description)
        ItemIndex.create(
            uuid=item2.uuid,
            name=item2.name,
            description=item2.description)
        ItemIndex.create(
            uuid=item3.uuid,
            name=item3.name,
            description=item3.description)

        query = "mariii OR GIOVANNI"
        resp = self.app.get('/items/db', query_string=query)
        items = json.loads(resp.data)

        assert resp.status_code == OK
        assert items[0]['uuid'] == item1.uuid
        assert items[0]['name'] == 'mario'
        assert items[1]['uuid'] == item3.uuid
        assert items[1]['name'] == 'GIOVANNI'
