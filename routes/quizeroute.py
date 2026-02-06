from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.quiz import Quiz
from app.utils.permissions import teacher_required

quiz_bp = Blueprint("quiz", __name__)
@quiz_bp.route("/quizzes", methods=["POST"])
@login_required
@teacher_required
def create_quiz():
    data = request.get_json()

    quiz = Quiz(
        title=data["title"],
        shuffle_questions=data.get("shuffle_questions", False),
        total_time_seconds=data.get("total_time_seconds"),
        created_by=current_user.id
    )

    db.session.add(quiz)
    db.session.commit()

    return jsonify({
        "quiz_id": quiz.id,
        "quiz_link": generate_quiz_link(quiz.id)
    }), 201
