from app.extensions import db
from datetime import datetime

class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)

    bank_id = db.Column(db.Integer, db.ForeignKey("question_banks.id"), nullable=False)

    type = db.Column(db.String(50), nullable=False)  # MCQ, TRUE_FALSE, TEXT
    content = db.Column(db.Text, nullable=False)
    hint = db.Column(db.Text)

    base_time = db.Column(db.Integer, nullable=False)  # seconds
    points = db.Column(db.Float, default=1)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    quiz_questions = db.relationship("QuizQuestion", backref="question", lazy=True)
    choices = db.relationship("Choice", backref="question", cascade="all, delete-orphan")



class Choice(db.Model):
    __tablename__ = "choices"
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
