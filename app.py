import os
import redis
from rq import Queue

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from blocklist import BLOCKLIST
from db import db

from resources.item import blue as ItemBlueprint
from resources.store import blue as StoreBlueprint
from resources.tag import blue as TagBlueprint
from resources.user import blue as UserBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    connection = redis.from_url(
        os.getenv("REDIS_URL")
    )

    app.queue = Queue("emails",connection=connection)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Store REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    # secrets.SystemRandom().getrandbits(128)
    app.config["JWT_SECRET_KEY"] = 'much-secure-key'
    db.init_app(app)
    migrate = Migrate(app,db)

    jwt = JWTManager(app)

    # Har safar token kelgan ushbu funksiya chaqiriladi, agarda funksiya True bo'lsa token hatolik qaytariladi
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    # Token bloklangan bo'lsa hatolik habarini ushbu funksiya yordamida qaytarsa bo'ladi
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (jsonify({
            "description": "The token has been revoked",
            "error": "token_revoked"
        }), 401)

     # Agar yangi token (fresh=True) so'ralganda token (fresh=False) bo'lsa foydalanuvchiga hatolik habarini qaytarish
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (jsonify({
                "description": "The token is not fresh.2222",
                "error": "fresh_token_required"
            }), 401)


    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (jsonify({
            'message': 'The token has expired.',
            'error': 'token_expired'
        }), 401)

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print("Error=>", error)
        return (jsonify({"message": "Signature verification failed.", "error": "invalid_token"}))

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({"description": "Request does not contain an access token.", "error": "authorization_required"}))

    api = Api(app)
    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    return app
