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

ITEM4 = {
    'uuid': 'd961c448-0f41-4932-8ce8-eede7e97dbbf',
    'name': 'giovanni mario',
    'price': 10.20,
    'description': 'GIOVANNI',
    'availability': 3,
}

ITEM5 = {
    'uuid': '5b6da961-db2d-489a-a765-e0463b938a89',
    'name': 'GIOVANNI  mario mario mario mario mario',
    'price': 10.20,
    'description': 'svariati',
    'availability': 3,
}


class TestItemsSearch(TestCase):

    def test_get_items_search__failed(self):
        item1 = Item.create(**ITEM1)

        ItemIndex.create(
            docid=item1.id,
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
            docid=item1.id,
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
            docid=item1.id,
            name=item1.name,
            description=item1.description)
        ItemIndex.create(
            docid=item2.id,
            name=item2.name,
            description=item2.description)
        ItemIndex.create(
            docid=item3.id,
            name=item3.name,
            description=item3.description)

        query = "mariii"
        resp = self.app.get('/items/db', query_string=query)
        items = json.loads(resp.data)

        assert resp.status_code == OK
        assert len(items) == 1
        assert items[0]['uuid'] == item1.uuid
        assert items[0]['name'] == 'mario'

    def test_get_items_search__success_OR_case(self):
        item1 = Item.create(**ITEM1)
        item2 = Item.create(**ITEM2)
        item3 = Item.create(**ITEM3)

        ItemIndex.create(
            docid=item1.id,
            name=item1.name,
            description=item1.description)
        ItemIndex.create(
            docid=item2.id,
            name=item2.name,
            description=item2.description)
        ItemIndex.create(
            docid=item3.id,
            name=item3.name,
            description=item3.description)

        query = "mariii OR GIOVANNI"
        resp = self.app.get('/items/db', query_string=query)
        items = json.loads(resp.data)

        assert resp.status_code == OK
        assert len(items) == 2
        assert items[0]['uuid'] == item3.uuid
        assert items[0]['name'] == 'GIOVANNI'
        assert items[1]['uuid'] == item1.uuid
        assert items[1]['name'] == 'mario'

    def test_get_items_search__ranking_success(self):
        item4 = Item.create(**ITEM4)
        item5 = Item.create(**ITEM5)

        ItemIndex.create(
            docid=item4.id,
            name=item4.name,
            description=item4.description)
        ItemIndex.create(
            docid=item5.id,
            name=item5.name,
            description=item5.description)

        query = "mario"
        resp = self.app.get('/items/db', query_string=query)
        items = json.loads(resp.data)
