from app.extensions import db
from datetime import datetime

class QuestionBank(db.Model):
    __tablename__ = "question_banks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    questions = db.relationship("Question", backref="bank", lazy=True)
