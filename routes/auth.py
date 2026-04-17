from flask import Blueprint, jsonify, request, current_app
from model import create_user, get_all_users, get_user_by_username, format_users
from werkzeug.security import generate_password_hash, check_password_hash
from utils.jwt_required import token_required
import jwt
import datetime

auth = Blueprint("auth", __name__)

#Register User
@auth.route("/register" , methods= ["POST"])
def add_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"message" : "Username dan password wajib diisi"}) , 400
    create_user(username, generate_password_hash(password))
    return jsonify({"message": "User berhasil dibuat"})

#Get Users
@auth.route("/users", methods= ["GET"])
def get_users():
    rows = get_all_users()
    return jsonify(format_users(rows))

#Login
@auth.route("/login", methods= ["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Input tidak valid"}) , 400
    username = data.get("username") 
    password = data.get("password")
    if not username or not password:
        return jsonify({"message": "Masukan username dan password"}), 400
    user = get_user_by_username(username)
    if not user:
        return jsonify({"message": "Username tidak ditemukan"}), 404
    token = jwt.encode({
        "user_id" : user[0],
        "exp" : datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        current_app.config["SECRET_KEY"],algorithm="HS256")
    if check_password_hash(user[2],password):
        return jsonify({
        "message": "Login berhasil",
        "token" : token
        }), 200
    else:
        return jsonify({"message": "Password salah"}), 401

@auth.route("/profile", methods=["GET"])
@token_required
def profile(id):
    return jsonify({
        "message": "Akses diterima",
        "user_id" : id
        }), 200
