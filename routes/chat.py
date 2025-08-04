# file: routes/chat.py
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from models import db, Room

chat_bp = Blueprint("chat", __name__, template_folder="../templates")

@chat_bp.route("/rooms", methods=["GET", "POST"])
@login_required
def chat_rooms():
    if request.method == "POST":
        room_name = request.form["room_name"]
        if not Room.query.filter_by(name=room_name).first():
            room = Room(name=room_name)
            db.session.add(room)
            db.session.commit()
        return redirect(url_for("chat.chat_room", room_id=room_name))
    rooms = Room.query.all()
    return render_template("rooms.html", rooms=rooms)


@chat_bp.route("/room/<string:room_id>")
@login_required
def chat_room(room_id):
    room = Room.query.filter_by(name=room_id).first_or_404()
    return render_template("chat.html", room=room)
