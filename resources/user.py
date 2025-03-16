
from flask import current_app
from db import db
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256

from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
from blocklist import BLOCKLIST
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

from models import UserModel
from schemas import UserSchema, UserRegisterSchema
from tasks import send_email_user_registration


blue = Blueprint('users', __name__, description="Operations on users")





@blue.route('/register')
class UserRegister(MethodView):
    @blue.arguments(UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(
                or_(UserModel.username==user_data['username'],
                    UserModel.email==user_data['email']
                    )
        ).first():
            abort(409, message="A user with that username or email already exists.")
        user = UserModel(
            username=user_data['username'],
            email=user_data['email'],
            password=pbkdf2_sha256.hash(user_data['password']))
        try:
            db.session.add(user)
            db.session.commit()
            print('===>')
            current_app.queue.enqueue(send_email_user_registration, user.email, user.username)



           
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return {"message": "User created", "id": user.id}



@blue.route('/login')
class UserLogin(MethodView):
    @blue.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter_by(username=user_data['username']).first()

        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            is_admin = user.id == 1
            access_token = create_access_token(identity=str(user.id), additional_claims={"is_admin": is_admin},
                                               fresh=True)
            refresh_token = create_refresh_token(identity=str(user.id))
            return {"access_token": access_token, "refresh_token": refresh_token}

        abort(401, message="Invalid credentials")


@blue.route('/refresh')
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt().get("jti")
        BLOCKLIST.add(jti)
        return {"access_token": new_token}


@blue.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt().get("jti")
        BLOCKLIST.add(jti)

        return {"message": "Logged out"}


@blue.route('/user/<int:user_id>')
class User(MethodView):
    @blue.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return {"message": "User deleted"}, 200

@blue.route('/user')
class UserList(MethodView):
    @blue.response(201, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()
