from app.extensions import db
from datetime import datetime
import uuid

class Quiz(db.Model):
    __tablename__ = "quizzes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    total_time = db.Column(db.Integer, nullable=False)  # seconds
    is_published = db.Column(db.Boolean, default=False)

    access_code = db.Column(
        db.String(36),
        unique=True,
        default=lambda: str(uuid.uuid4())
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    questions = db.relationship("QuizQuestion", backref="quiz", lazy=True)
    attempts = db.relationship("QuizAttempt", backref="quiz", lazy=True)
    time_type = db.Column(db.String, default="fixed")  # أو "open" حسب رغبتك


class QuizQuestion(db.Model):
    __tablename__ = "quiz_questions"

    id = db.Column(db.Integer, primary_key=True)

    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)

    order = db.Column(db.Integer, nullable=False)
