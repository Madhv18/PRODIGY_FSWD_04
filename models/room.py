from models import db, TimestampMixin

class Room(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    messages = db.relationship("Message", back_populates="room", lazy=True)
