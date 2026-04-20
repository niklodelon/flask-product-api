# 🛒 Flask Product API

REST API sederhana menggunakan Flask + SQLite dengan fitur authentication (JWT).

## 🚀 Features
- Register & Login (JWT)
- CRUD Produk
- Search Produk
- Filter Harga
- Sorting Produk
- Total Produk

## 🔐 Authentication
Menggunakan JWT Token

## 🛠 Tech Stack
- Python
- Flask
- SQLite
- JWT

## 📦 Endpoint

### Auth
POST /register  
POST /login  

### Products
GET /products  
POST /products  
PUT /products/<id>  
DELETE /products/<id>  

## ▶️ Cara Menjalankan

```bash
pip install -r requirements.txt
python app.py
