import jwt

data = {"user": "deden"}

token = jwt.encode(data, "secJHAJFE637W87Q238NFANVKNNVJS862378578JKBKVBret", algorithm="HS256")

print(token)

try:
        data = jwt.decode(token,app.config["SECRET_KEY"],algorithm=["HS256"])
    except:
        return jsonify({"message": "Password salah"})
    user_id = data["user_id"]

    return jsonify({
        "message": "Akses diterima",
        "user_id" : user_id
        }), 200

    return jsonify({"message": "Password salah"})
