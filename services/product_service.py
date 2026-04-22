from flask import jsonify, request
from model import insert_product, update_product_byid, del_product

def add_product_logic(data):
    if not data:
        return False, "Input Tidak Valid"
    if "nama" not in data:
        return False, "Masukkan nama"
    try :
        harga = int(data["harga"])
        stok = int(data["stok"])
    except (ValueError, TypeError):
        return False, "Input Tidak Valid"
    insert_product(data["nama"],harga,stok)	
    return True, "Produk Ditambahkan"

def update_product_logic(data,id):
	if not data:
		return False, "Input Tidak Valid"
	if "nama" not in data:
		return False, "Masukkan nama"
	try :
		harga = int(data["harga"])
		stok = int(data["stok"])
	except (ValueError, TypeError):
		return False, "Input Tidak Valid"
	update_product_byid(data["nama"],harga,stok,id)
	return True, "Produk Diupdate"

def delete_product_logic(id):
	del_product(id)
	return True, "Produk Berhasil Dihapus"