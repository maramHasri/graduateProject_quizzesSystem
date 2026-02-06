from flask import Flask
from app.extensions import db, migrate, jwt
from app.config import Config
from app.api import api
from app.api.quiz import quiz_ns
from app.api.auth import auth_ns    

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Swagger / API
    api.init_app(app)
    api.add_namespace(quiz_ns, path="/api/quizzes")
    api.add_namespace(auth_ns, path="/api/auth")  # <--- هنا تأكد المسار صحيح

    return app
