# file: app.py
from flask import Flask, request, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from config import Config
from models import db, User, Room, Message
from flask_login import current_user

socketio = SocketIO(cors_allowed_origins="*")  # CORS wide-open for dev

login_manager = LoginManager()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Plug-ins
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)

    # Blueprints
    from routes.auth import auth_bp
    from routes.chat import chat_bp
    from routes.api import api_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    # Simple landing
    @app.route("/")
    def index():
        return render_template("index.html")

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -------------- Socket.IO EVENTS ---------------
@socketio.on("connect")
def handle_connect():
    if current_user.is_authenticated:
        emit("status", {"msg": f"{current_user.username} connected."})
    else:
        emit("status", {"msg": "Guest connected."})


@socketio.on("join")
def handle_join(data):
    room = data.get("room")
    join_room(room)
    emit(
        "status",
        {"msg": f"{current_user.username} has entered the room."},
        room=room,
    )


@socketio.on("leave")
def handle_leave(data):
    room = data.get("room")
    leave_room(room)
    emit(
        "status",
        {"msg": f"{current_user.username} has left the room."},
        room=room,
    )


@socketio.on("send_message")
def handle_message(data):
    room = data["room"]
    msg_text = data["message"]

    # Persist to DB
    message = Message(
        author_id=current_user.id,
        room_id=room,
        content=msg_text
    )
    db.session.add(message)
    db.session.commit()

    emit(
        "receive_message",
        {
            "user": current_user.username,
            "msg": msg_text,
            "timestamp": message.created_at.isoformat(),
        },
        room=room,
    )


if __name__ == "__main__":
    app = create_app()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
