from flask import abort, request
from flask_restful import Resource
from http.client import (CREATED, NO_CONTENT, NOT_FOUND, OK, BAD_REQUEST, UNAUTHORIZED)


class ItemsSearchHandler(Resource):

    def get(self):
        return [o.json() for o in Item.select()], OK
