from flask import Blueprint, jsonify, request, current_app
from model import get_all_products, get_product_byid, select_nama, select_max, select_by_sort, count_total, format_products
from services.product_service import add_product_logic, update_product_logic, delete_product_logic
from utils.jwt_required import token_required

product = Blueprint("product", __name__)

#Add Product
@product.route("/products", methods =["POST"])
@token_required
def add_product(user_id):
    data = request.get_json()
    success, message = add_product_logic(data)
    if not success:
    	return jsonify({"message" : message}, 400)
    else:
    	return jsonify({"message" : message}, 201)

#Get All Product
@product.route("/products", methods=["GET"])
@token_required
def get_products(user_id):
    rows = get_all_products()
    return jsonify(format_products(rows))


#Get Product by Id
@product.route("/products/<int:id>", methods=["GET"])
@token_required
def get_product(user_id, id):
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
@product.route("/products/<int:id>", methods=["PUT"])
@token_required
def update_product(user_id, id):
    data = request.get_json()
    success, message = update_product_logic(data,id)
    if not success:
    	return jsonify({"message" : message}, 400)
    else:
    	return jsonify({"message" : message}, 200)


#Delete Product
@product.route("/products/<int:id>", methods=["DELETE"])
@token_required
def delete_product(user_id, id):
    success, message = delete_product_logic(id)
    if not success:
    	return jsonify({"message" : message}, 400)
    else:
    	return jsonify({"message" : message}, 200)

#Search Product by name
@product.route("/products/search", methods=["GET"])
@token_required
def search_product(user_id):
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
@product.route("/products/filter", methods=["GET"])
@token_required
def filter_harga(user_id):
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
@product.route("/products/sort", methods=["GET"])
@token_required
def sort_products(user_id):
    order = request.args.get("order")
    if not order:
        return jsonify({"message" : "Order tidak valid"} , 400)
    if order not in ["asc", "desc"]:
        return jsonify({"message" : "Order tidak valid"} , 400)
    rows = select_by_sort(order)
    return jsonify(format_products(rows))

@product.route("/products/total", methods=["GET"])
@token_required
def total_products(user_id):
    rows = count_total()
    total = rows[0]
    return jsonify({"total": total})