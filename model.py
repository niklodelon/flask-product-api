from database import conn, cursor

def create_user(username, password):
	cursor.execute(
	"INSERT INTO users (username, password) VALUES (?,?)",
		(username, password)
)
	conn.commit()

def get_all_users():
	cursor.execute("SELECT * FROM users")
	return cursor.fetchall()

def get_user_by_username(username):
	cursor.execute("SELECT * FROM users WHERE username = ?",(username,))
	return cursor.fetchone()

def format_users(rows):
	users = []
	for r in rows:
		users.append({
			"id": r[0],
			"username": r[1]
			
		})
	return users   

def format_products(rows):
	products = []
	for r in rows:
		products.append({
			"id": r[0],
			"nama": r[1],
			"harga": r[2],
			"stok": r[3]
		})
	return products        


def get_all_products():
	cursor.execute("SELECT * FROM products")
	return cursor.fetchall()

def insert_product(nama,harga,stok):
	cursor.execute(
	"INSERT INTO products (nama,harga,stok) VALUES (?,?,?)",
		(nama,harga,stok)
)
	conn.commit()

def get_product_byid(id):
	cursor.execute("SELECT * FROM products WHERE  id = ?",(id,))
	return cursor.fetchone()
   
def update_product_byid(nama,harga,stok,id):
	cursor.execute(
		"UPDATE products SET nama = ?, harga = ?, stok = ? WHERE id = ?",
		(nama,harga,stok,id)
		)
	conn.commit()

def del_product(id):
	cursor.execute("DELETE FROM products WHERE id = ?", (id,))
	conn.commit()

def select_nama(nama):
	cursor.execute("SELECT * FROM products WHERE nama LIKE ?",
		("%" + nama + "%",)
	)
	return cursor.fetchall()

def select_max(maxHarga):
	cursor.execute("SELECT * FROM products WHERE harga <= ?",(maxHarga,))
	return cursor.fetchall()

def select_by_sort(order):
	if order == "asc":
		cursor.execute("SELECT * FROM products ORDER BY harga ASC")
	elif order == "desc":
		cursor.execute("SELECT * FROM products ORDER BY harga DESC")
	return cursor.fetchall()

def count_total():
	cursor.execute("SELECT COUNT(*) FROM products")
	return cursor.fetchone()
    
