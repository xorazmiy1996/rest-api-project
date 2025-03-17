from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, PlainTagSchema, TagAndItemSchema

blue = Blueprint('Tags', __name__, description='Operations on tags')


@blue.route('/store/<int:store_id>/tag')
class TagInStore(MethodView):
    @jwt_required()
    @blue.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @jwt_required()
    @blue.arguments(PlainTagSchema)
    @blue.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter_by(store_id=store_id, name=tag_data['name']).first():
            abort(400, message="A tag with that name already exists.")

        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag, 201


@blue.route('/item/<int:item_id>/tag/<int:tag_id>')
class LinkTagsToItem(MethodView):
    @jwt_required()
    @blue.response(200, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.appent(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while linking the tag to the item")
        return tag

    @jwt_required()
    @blue.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while unlinking the tag from the item")
        return {"message": "Tag removed from tag", "tag": tag, "item": item}


@blue.route('/tag/<int:tag_id>')
class Tag(MethodView):
    @jwt_required()
    @blue.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @jwt_required()
    @blue.response(202, description="Delete a tag if no item is tagged with it.", example={"message": "Tag deleted"})
    @blue.alt_response(400, description="Tag not found")
    @blue.response(400,
                   description="Returned if the is assigned to one or more items. In this case, the tag is not deleted")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted"}
        abort(400, message="Tag cannot be deleted because it is linked to an item")
