from database import conn, cursor, init_db
from flask import Flask
from routes.auth import auth
from routes.product import product
import os

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(product)
app.config["SECRET_KEY"] = "password_rahasia_delon"

try:
    init_db()
except Exception as e:
    print("DB ERROR:", e)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)