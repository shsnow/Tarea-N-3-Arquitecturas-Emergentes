from flask import Flask, request, jsonify, g
from models import init_db, get_db
import sqlite3
import uuid
import hashlib

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/api/v1/admin/company', methods=['POST'])
def create_company():
    data = request.get_json()
    company_name = data.get('company_name')
    company_api_key = str(uuid.uuid4())
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO company (company_name, company_api_key) VALUES (?, ?)', (company_name, company_api_key))
    conn.commit()
    
    return jsonify({"company_api_key": company_api_key}), 201

@app.route('/api/v1/company/<int:company_id>/location', methods=['POST'])
def create_location(company_id):
    data = request.get_json()
    location_name = data.get('location_name')
    location_country = data.get('location_country')
    location_city = data.get('location_city')
    location_meta = data.get('location_meta')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO location (company_id, location_name, location_country, location_city, location_meta) VALUES (?, ?, ?, ?, ?)',
                   (company_id, location_name, location_country, location_city, location_meta))
    conn.commit()
    
    return jsonify({"message": "Location created"}), 201

@app.route('/api/v1/location/<int:location_id>/sensor', methods=['POST'])
def create_sensor(location_id):
    data = request.get_json()
    sensor_name = data.get('sensor_name')
    sensor_category = data.get('sensor_category')
    sensor_meta = data.get('sensor_meta')
    sensor_api_key = str(uuid.uuid4())
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO sensor (location_id, sensor_name, sensor_category, sensor_meta, sensor_api_key) VALUES (?, ?, ?, ?, ?)',
                   (location_id, sensor_name, sensor_category, sensor_meta, sensor_api_key))
    conn.commit()
    
    return jsonify({"sensor_api_key": sensor_api_key}), 201

@app.route('/api/v1/sensor_data', methods=['POST'])
def insert_sensor_data():
    data = request.get_json()
    api_key = data.get('api_key')
    json_data = data.get('json_data')
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM sensor WHERE sensor_api_key = ?', (api_key,))
    sensor = cursor.fetchone()
    
    if not sensor:
        return jsonify({"error": "Invalid API key"}), 400
    
    sensor_id = sensor[0]
    
    for entry in json_data:
        cursor.execute('INSERT INTO sensor_data (sensor_id, timestamp, data) VALUES (?, strftime("%s", "now"), ?)', (sensor_id, str(entry)))
    
    conn.commit()
    
    return jsonify({"message": "Data inserted"}), 201

@app.route('/api/v1/sensor_data', methods=['GET'])
def get_sensor_data():
    company_api_key = request.args.get('company_api_key')
    from_epoch = request.args.get('from')
    to_epoch = request.args.get('to')
    sensor_ids = request.args.getlist('sensor_id')
    
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM company WHERE company_api_key = ?', (company_api_key,))
    company = cursor.fetchone()
    
    if not company:
        return jsonify({"error": "Invalid API key"}), 400
    
    query = 'SELECT * FROM sensor_data WHERE timestamp BETWEEN ? AND ? AND sensor_id IN ({})'.format(','.join('?' * len(sensor_ids)))
    cursor.execute(query, [from_epoch, to_epoch] + sensor_ids)
    
    sensor_data = cursor.fetchall()
    
    result = [{"sensor_id": row["sensor_id"], "timestamp": row["timestamp"], "data": row["data"]} for row in sensor_data]
    
    return jsonify(result)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
