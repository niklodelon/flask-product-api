from database import conn, cursor, init_db
from flask import Flask, jsonify, request
from routes.auth import auth
from routes.product import product
import os

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(product)
app.config["SECRET_KEY"] = "password_rahasia_delon"

init_db()

if __name__ == "__main__":
    app.run(debug=True)
