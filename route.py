from database import conn, cursor, init_db
from flask import Flask, jsonify, request
from model import get_all_products, insert_product, get_product_byid, update_product_byid, del_product, select_nama, select_max, select_by_sort, count_total, format_products, create_user, get_all_users, get_user_by_username, format_users
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = "password_rahasia_delon"

init_db()
#Register User
@app.route("/register" , methods= ["POST"])
def add_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"message" : "Username dan password wajib diisi"}) , 400
    create_user(username, generate_password_hash(password))
    return jsonify({"message": "User berhasil dibuat"})

#Get Users
@app.route("/users", methods= ["GET"])
def get_users():
    rows = get_all_users()
    return jsonify(format_users(rows))

#Login
@app.route("/login", methods= ["POST"])
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
        app.config["SECRET_KEY"],algorithm="HS256")
    if check_password_hash(user[2],password):
        return jsonify({
        "message": "Login berhasil",
        "token" : token
        }), 200
    else:
        return jsonify({"message": "Password salah"}), 401

@app.route("/profile", methods=["GET"])
def profile():
    auth_header = request.headers.get("Authorization")    
    if not auth_header:
        return jsonify({"message": "Token tidak valid"})
    token = auth_header.split(" ")[1]
    try:
        data = jwt.decode(token,app.config["SECRET_KEY"],algorithms=["HS256"])
    except:
        return jsonify({"message": "Token tidak valid"})

    user_id = data["user_id"]
    return jsonify({
        "message": "Akses diterima",
        "user_id" : user_id
        }), 200
    
#Add Product
@app.route("/products", methods =["POST"])
def add_product():
    data = request.get_json()
    #Validasi request
    if not data:
        return jsonify({"message" : "Input tidak valid"}) , 400
    if "nama" not in data:
        return jsonify({"message" : "Masukkan nama"}), 400
    try :
        harga = int(data["harga"])
        stok = int(data["stok"])
    except (ValueError, TypeError):
        return jsonify({"message" : "Input tidak valid"} , 400)

    insert_product(data["nama"],harga,stok)
    return jsonify({"message": "Produk ditambahkan"})

#Get All Products
@app.route("/products", methods=["GET"])
def get_products():
    rows = get_all_products()
    return jsonify(format_products(rows))

#Get Product by Id
@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = get_product_byid(id)
    if product:
        return jsonify({
            "id": product[0],
            "nama": product[1],
            "harga": product[2],
            "stok" : product[3]
            })
    return jsonify({ "message" : "Produk tidak ditemukan"}), 404

#Update Product
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    data = request.get_json()
    if not data:
        return jsonify({"message" : "Input tidak valid"} , 400)
    if "nama" not in data:
        return jsonify({"message" : "Masukan nama"}) , 400
    try :
        harga = int(data["harga"])
        stok = int(data["stok"])
    except (ValueError, TypeError):
        return jsonify({"message" : "Input tidak valid"} , 400)

    update_product_byid(data["nama"],harga,stok,id)
    return jsonify({"message": "Produk berhasil diupdate"})

#Delete Product
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    del_product(id)
    return jsonify({"message": "Produk berhasil dihapus"})

#Search Product by name
@app.route("/products/search", methods=["GET"])
def search_product():
    nama = request.args.get("nama")
    if not nama:
        return jsonify({"message" : "Nama wajib diisi"} , 400)
    rows = select_nama(nama)
    if not rows:
        return jsonify({
            "message" : "Barang tidak ditemukan"
            }) , 404
    return jsonify(format_products(rows))

#Filter Product
@app.route("/products/filter", methods=["GET"])
def filter_harga():
    maxHarga = request.args.get("max")
    #Validation maxHarga
    if not maxHarga:
        return jsonify({"message" : "Masukan Maks Harga"} , 400)
    try :
        maxHarga = int(maxHarga)
    except (TypeError, ValueError):
         return jsonify({"message" : "Input tidak valid"} , 400)
    rows = select_max(maxHarga)
    if not rows:
        return jsonify({
            "message" : "Barang tidak ditemukan"
            }) , 404
    return jsonify(format_products(rows))

#Sorting Product
@app.route("/products/sort", methods=["GET"])
def sort_products():
    order = request.args.get("order")
    if not order:
        return jsonify({"message" : "Order tidak valid"} , 400)
    if order not in ["asc", "desc"]:
        return jsonify({"message" : "Order tidak valid"} , 400)
    rows = select_by_sort(order)
    return jsonify(format_products(rows))

@app.route("/products/total", methods=["GET"])
def total_products():
    rows = count_total()
    total = rows[0]
    return jsonify({"total": total})

if __name__ == "__main__":
	app.run(debug=True)
