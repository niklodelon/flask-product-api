from flask import Blueprint, jsonify, request, current_app
from model import get_all_products, insert_product, get_product_byid, update_product_byid, del_product, select_nama, select_max, select_by_sort, count_total, format_products

product = Blueprint("product", __name__)

#Get All Product
@product.route("/products", methods=["GET"])
def get_products():
    rows = get_all_products()
    return jsonify(format_products(rows))


#Add Product
@product.route("/products", methods =["POST"])
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

#Get Product by Id
@product.route("/products/<int:id>", methods=["GET"])
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
@product.route("/products/<int:id>", methods=["PUT"])
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
@product.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    del_product(id)
    return jsonify({"message": "Produk berhasil dihapus"})

#Search Product by name
@product.route("/products/search", methods=["GET"])
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
@product.route("/products/filter", methods=["GET"])
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
@product.route("/products/sort", methods=["GET"])
def sort_products():
    order = request.args.get("order")
    if not order:
        return jsonify({"message" : "Order tidak valid"} , 400)
    if order not in ["asc", "desc"]:
        return jsonify({"message" : "Order tidak valid"} , 400)
    rows = select_by_sort(order)
    return jsonify(format_products(rows))

@product.route("/products/total", methods=["GET"])
def total_products():
    rows = count_total()
    total = rows[0]
    return jsonify({"total": total})