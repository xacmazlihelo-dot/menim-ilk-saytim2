from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Verilənlər bazasını yaradan funksiya
def init_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return jsonify({
        "status": "success",
        "message": "Azure VM-də Python Flask API uğurla işləyir!",
        "version": "2.0"
    })

# Bütün məlumatları gətirən GET endpoint-i
@app.route('/api/items', methods=['GET'])
def get_items():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    rows = cursor.fetchall()
    conn.close()
    
    items = [{"id": row[0], "name": row[1]} for row in rows]
    return jsonify({"status": "success", "data": items})

# Yeni məlumat əlavə edən POST endpoint-i
@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"status": "error", "message": "Name parametri vacibdir"}), 400
    
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO items (name) VALUES (?)', (data['name'],))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "Məlumat bazaya əlavə edildi"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)