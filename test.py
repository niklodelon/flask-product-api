user_id = data["user_id"]
    return jsonify({
        "message": "Akses diterima",
        "user_id" : user_id
        }), 200

di jwt_required
import jwt
from flask import jsonify, request
def token_required(f):
    def decorator():
        auth_header = request.headers.get("Authorization")  
        if not auth_header:
            return jsonify({"message": "Token tidak valid"})
        token = auth_header.split(" ")[1]
        data = jwt.decode(token,app.config["SECRET_KEY"],algorithms=["HS256"])
        if not data:
            return jsonify({"message": "Token tidak valid"})
        user_id = data["user_id"]
    return f

di route
@app.route("/profile", methods=["GET"])
@token_required
def profile():
    return jsonify({
        "message": "Akses diterima",
        }), 200