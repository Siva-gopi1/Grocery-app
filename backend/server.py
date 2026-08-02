import os
import sys

# Ensure sibling modules are importable when run from project root (e.g. Vercel/Railway)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, send_from_directory
from sql_connection import get_sql_connection
import mysql.connector
import json

import products_dao
import orders_dao
import uom_dao

# Resolve the path to the ui/ directory (one level up from backend/)
UI_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ui')

app = Flask(__name__, static_folder=UI_DIR, static_url_path='')

connection = None


def get_db_connection():
    global connection
    if connection is None or not connection.is_connected():
        connection = get_sql_connection()
    return connection


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# ---------- Serve UI pages ----------

@app.route('/')
def serve_index():
    return send_from_directory(UI_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(UI_DIR, filename)

# ---------- API routes ----------
# Each endpoint is registered twice: once without prefix (for local dev)
# and once with /api prefix (for deployed frontend via common.js)

@app.route('/getUOM', methods=['GET'])
@app.route('/api/getUOM', methods=['GET'])
def get_uom():
    response = uom_dao.get_uoms(get_db_connection())
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getProducts', methods=['GET'])
@app.route('/api/getProducts', methods=['GET'])
def get_products():
    response = products_dao.get_all_products(get_db_connection())
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertProduct', methods=['POST'])
@app.route('/api/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(get_db_connection(), request_payload)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getAllOrders', methods=['GET'])
@app.route('/api/getAllOrders', methods=['GET'])
def get_all_orders():
    response = orders_dao.get_all_orders(get_db_connection())
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getDashboardSummary', methods=['GET'])
@app.route('/api/getDashboardSummary', methods=['GET'])
def get_dashboard_summary():
    summary = orders_dao.get_dashboard_summary(get_db_connection())
    response = jsonify(summary)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertOrder', methods=['POST'])
@app.route('/api/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = orders_dao.insert_order(get_db_connection(), request_payload)
    response = jsonify({
        'order_id': order_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/deleteProduct', methods=['POST'])
@app.route('/api/deleteProduct', methods=['POST'])
def delete_product():
    return_id = products_dao.delete_product(get_db_connection(), request.form['product_id'])
    response = jsonify({
        'product_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '5000'))
    app.run(host=host, port=port)
