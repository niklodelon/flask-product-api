import jwt
from flask import jsonify, request, current_app
from functools import wraps

def token_required(f):
	@wraps(f)
	def decorator(*args, **kwargs):
		auth_header = request.headers.get("Authorization")  
		if not auth_header:
			return jsonify({"message": "Token tidak ada"}), 401
		token = auth_header.split(" ")[1]
		try :
			data = jwt.decode(token,current_app.config["SECRET_KEY"],algorithms=["HS256"])
		except:
			return jsonify({"message": "Token tidak valid"}), 401
		user_id = data["user_id"]
		return f(user_id, *args, **kwargs)
	return decorator