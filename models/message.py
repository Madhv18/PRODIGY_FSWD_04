from models import db, TimestampMixin
from datetime import datetime

class Message(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"))

    author = db.relationship("User", back_populates="messages")
    room = db.relationship("Room", back_populates="messages")
