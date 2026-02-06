from flask_restx import Namespace, Resource, fields
from flask import request
from app.extensions import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_ns = Namespace("Auth", description="Authentication & Authorization")

# 🔹 نموذج تسجيل حساب
register_model = auth_ns.model(
    "Register",
    {
        "name": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True),
        "role": fields.String(required=True, description="teacher | student | admin")
    }
)

# 🔹 نموذج تسجيل الدخول
login_model = auth_ns.model(
    "Login",
    {
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    }
)

# 🔹 نموذج الرد بعد تسجيل الدخول
token_model = auth_ns.model(
    "Token",
    {
        "token": fields.String
    }
)

# ===== تسجيل حساب =====
@auth_ns.route("/register")
class Register(Resource):
    @auth_ns.expect(register_model)
    def post(self):
        data = auth_ns.payload
        # تحقق من أن البريد غير موجود مسبقًا
        if User.query.filter_by(email=data["email"]).first():
            return {"message": "Email already exists"}, 400

        user = User(
            name=data["name"],
            email=data["email"],
            role=data["role"]
        )
        user.set_password(data["password"])

        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully"}, 201

# ===== تسجيل الدخول =====
@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.marshal_with(token_model)
    def post(self):
        data = auth_ns.payload
        user = User.query.filter_by(email=data["email"]).first()
        if not user or not user.check_password(data["password"]):
            return {"message": "Invalid email or password"}, 401

        # توليد JWT token
        access_token = create_access_token(identity={"id": user.id, "role": user.role})
        return {"token": access_token}, 200
