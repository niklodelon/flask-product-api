from flask import jsonify, request
from model import insert_product

def add_product_logic(data):
    if not data:
        return ({"message" : "Input tidak valid"}) , 400
    if "nama" not in data:
        return ({"message" : "Masukkan nama"}), 400
    try :
        harga = int(data["harga"])
        stok = int(data["stok"])
    except (ValueError, TypeError):
        return ({"message" : "Input tidak valid"} , 400)

    insert_product(data["nama"],harga,stok) 

    return ({"message": "Produk ditambahkan"})
