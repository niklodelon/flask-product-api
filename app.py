from database import conn, cursor, init_db
from flask import Flask, jsonify, request
from model import get_all_products, insert_product, get_product_byid, update_product_byid, del_product, select_nama, select_max, select_by_sort, count_total, format_products, create_user, get_all_users, get_user_by_username, format_users
from routes.auth import auth
from routes.product import product

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(product)
app.config["SECRET_KEY"] = "password_rahasia_delon"

init_db()

if __name__ == "__main__":
	app.run(debug=True)
