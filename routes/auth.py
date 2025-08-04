# file: routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from utils.auth_utils import hash_password, verify_password

auth_bp = Blueprint("auth", __name__, template_folder="../templates")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter((User.username == username)|(User.email == email)).first():
            flash("Username or email already exists.")
            return redirect(url_for("auth.register"))

        user = User(username=username, email=email,
                    password_hash=hash_password(password))
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and verify_password(password, user.password_hash):
            login_user(user)
            return redirect(url_for("chat.chat_rooms"))
        flash("Invalid credentials")
    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
