
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blue = Blueprint("Item",__name__,description="Operations on items")

@blue.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blue.response(201, ItemSchema)
    def get(self,item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self,item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privileges required")

        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message":"Item deleted"}


    @blue.arguments(ItemUpdateSchema)
    @blue.response(201, ItemSchema)
    def put(self,item_data,item_id):
        item = ItemModel.query.get_or_404(item_id)
        if item:
            item.price = item_data['price']
            item.name = item_data['name']
        else:
            item = ItemModel(**item_data)

        db.session.add(item)
        db.session.commit()
        return item


@blue.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blue.response(201, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
 
    @jwt_required(fresh=True)
    @blue.arguments(ItemSchema)
    @blue.response(201, ItemSchema())
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item")



        return item, 201
