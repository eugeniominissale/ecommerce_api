from flask import abort, request
from flask_restful import Resource
from http.client import (CREATED, NO_CONTENT, NOT_FOUND, OK, BAD_REQUEST, UNAUTHORIZED)
from models import Item, ItemIndex


class ItemsSearchHandler(Resource):

    def get(self):

        query = request.query_string.decode()

        if not query:
            return None, BAD_REQUEST

        res = (Item.select()
               .join(
               ItemIndex,
               on=(Item.uuid == ItemIndex.uuid))
               .where(ItemIndex.match(query))
               .order_by(ItemIndex.bm25()))

        if not res:
            return None, NOT_FOUND
        return [o.json() for o in res], OK
