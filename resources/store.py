import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema

blue = Blueprint("stores", __name__, description="Operations on stores")

@blue.route("/store/<int:store_id>")
class Store(MethodView):
    @jwt_required()
    @blue.response(201, StoreSchema)
    def get(self,store_id):
        item = StoreModel.query.get_or_404(store_id)
        return item
    def delete(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message":"Store deleted"}

@blue.route("/store")
class StoreList(MethodView):
    @jwt_required()
    @blue.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @jwt_required()
    @blue.arguments(StoreSchema)
    @blue.response(201, StoreSchema())
    def post(self, store_data):
        try:
            store = StoreModel(**store_data)
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists. ")

        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the store")

        return store, 201
