from flask import abort, request
from flask_restful import Resource
from http.client import (CREATED, NO_CONTENT, NOT_FOUND, OK, BAD_REQUEST, UNAUTHORIZED)
from models import Item, ItemIndex


class ItemsSearchHandler(Resource):

    def get(self):

        query = str(request.args[0])

        if not query:
            return BAD_REQUEST

        res = (Item.select()
               .join(
               ItemIndex,
               on=(Item.item_id == ItemIndex.item_id))
               .where(ItemIndex.match(query))
               .order_by(ItemIndex.bm25()))

        return list(res), OK
