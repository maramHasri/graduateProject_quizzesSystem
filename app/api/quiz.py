from flask_restx import Namespace, Resource, fields
from app.extensions import db
from app.models import Quiz, User
from datetime import datetime
import uuid

quiz_ns = Namespace("quizzes", description="Quiz management")

# 🔹 Swagger Model (Schema)
quiz_create_model = quiz_ns.model(
    "QuizCreate",
    {
        "title": fields.String(required=True),
        "description": fields.String,
        "total_time": fields.Integer(required=True),
        "creator_id": fields.Integer(required=True),
    }
)

quiz_response_model = quiz_ns.model(
    "QuizResponse",
    {
        "id": fields.Integer,
        "title": fields.String,
        "access_code": fields.String,
        "quiz_url": fields.String,
    }
)

@quiz_ns.route("")
class QuizCreate(Resource):

    @quiz_ns.expect(quiz_create_model)
    @quiz_ns.marshal_with(quiz_response_model, code=201)
    def post(self):
        """
        Create a new quiz (Teacher only)
        """
        data = quiz_ns.payload

        # 🔹 تحقق من وجود الـ creator قبل إنشاء الكويز
        creator = User.query.get(data["creator_id"])
        if not creator:
            return {"message": "Creator not found"}, 404

        # 🔹 إنشاء الكويز
        quiz = Quiz(
            title=data["title"],
            description=data.get("description"),
            total_time=data["total_time"],
                time_type=data.get("time_type", "open"),

            creator_id=creator.id,
            is_published=True,
            access_code=str(uuid.uuid4()),  # لضمان وجود access_code
            created_at=datetime.utcnow()
        )

        db.session.add(quiz)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # 🔹 رجّع الـ session لو صار خطأ
            return {"message": str(e)}, 400

        return {
            "id": quiz.id,
            "title": quiz.title,
            "access_code": quiz.access_code,
            "quiz_url": f"http://localhost:5000/quiz/{quiz.access_code}"
        }, 201
