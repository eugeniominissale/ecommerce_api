from flask import abort, request
from flask_restful import Resource
from http.client import (CREATED, NO_CONTENT, NOT_FOUND, OK, BAD_REQUEST, UNAUTHORIZED)
from models import Item, ItemIndex
from peewee import SQL


class ItemsSearchHandler(Resource):

    def get(self):

        query = request.query_string.decode()

        if not query:
            return None, BAD_REQUEST

        # 0 / -1 (best)
        # -0.83 / -0,17 (occorrenze >, stessa colonna)
        # -1.17 / -0.83 (1,1 / 5,0)
        # -1.17 / -0.83 (1,1 / 0,5)
        # -1 / -1 (1,0 /0,5)

        res = (Item
               .select(Item, ItemIndex, ItemIndex.rank().alias('score'))
               .join(ItemIndex,
                     on=(Item.id == ItemIndex.docid))
               .where(ItemIndex.match(query))
               .order_by(SQL('score').asc()))

        # for item in res:
        #     print(item.name, round(item.score, 2))

        # query = ItemIndex.search_bm25(query,
        #                               with_score=True).tuples()
        # res = [o for o in query]

        # print(res)
        # import pdb; pdb.set_trace()
        if not res:
            return None, NOT_FOUND
        return [o.json() for o in res], OK
