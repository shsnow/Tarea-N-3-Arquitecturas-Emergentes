from flask import Flask, request, jsonify, make_response
from database import db
from models import Admin, Company, Location, Sensor, SensorData
import uuid
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/api/v1/admin/company', methods=['POST'])
def create_company():
    data = request.get_json()
    company_name = data.get('company_name')
    if not company_name:
        return make_response(jsonify({"error": "Company name is required"}), 400)
    
    company_api_key = str(uuid.uuid4())
    new_company = Company(company_name=company_name, company_api_key=company_api_key)
    db.session.add(new_company)
    db.session.commit()
    
    return make_response(jsonify({"message": "Company created successfully", "company_api_key": company_api_key}), 201)

@app.route('/api/v1/companies', methods=['GET'])
def get_companies():
    companies = Company.query.all()
    output = []
    for company in companies:
        company_data = {'id': company.id, 'company_name': company.company_name, 'company_api_key': company.company_api_key}
        output.append(company_data)
    return jsonify({'companies': output})

@app.route('/api/v1/company/<company_id>', methods=['GET'])
def get_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        return make_response(jsonify({"error": "Company not found"}), 404)
    company_data = {'id': company.id, 'company_name': company.company_name, 'company_api_key': company.company_api_key}
    return jsonify(company_data)

@app.route('/api/v1/company/<company_id>', methods=['PUT'])
def update_company(company_id):
    data = request.get_json()
    company = Company.query.get(company_id)
    if not company:
        return make_response(jsonify({"error": "Company not found"}), 404)
    company.company_name = data.get('company_name', company.company_name)
    db.session.commit()
    return jsonify({"message": "Company updated successfully"})

@app.route('/api/v1/company/<company_id>', methods=['DELETE'])
def delete_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        return make_response(jsonify({"error": "Company not found"}), 404)
    db.session.delete(company)
    db.session.commit()
    return jsonify({"message": "Company deleted successfully"})

@app.route('/api/v1/admin/location', methods=['POST'])
def create_location():
    data = request.get_json()
    company_id = data.get('company_id')
    company = Company.query.get(company_id)
    if not company:
        return make_response(jsonify({"error": "Company not found"}), 404)

    location_name = data.get('location_name')
    location_country = data.get('location_country')
    location_city = data.get('location_city')
    location_meta = data.get('location_meta')
    
    new_location = Location(company_id=company_id, location_name=location_name, location_country=location_country,
                            location_city=location_city, location_meta=location_meta)
    db.session.add(new_location)
    db.session.commit()
    
    return make_response(jsonify({"message": "Location created successfully"}), 201)

@app.route('/api/v1/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    output = []
    for location in locations:
        location_data = {'id': location.id, 'company_id': location.company_id, 'location_name': location.location_name,
                         'location_country': location.location_country, 'location_city': location.location_city, 'location_meta': location.location_meta}
        output.append(location_data)
    return jsonify({'locations': output})

@app.route('/api/v1/location/<location_id>', methods=['GET'])
def get_location(location_id):
    location = Location.query.get(location_id)
    if not location:
        return make_response(jsonify({"error": "Location not found"}), 404)
    location_data = {'id': location.id, 'company_id': location.company_id, 'location_name': location.location_name,
                     'location_country': location.location_country, 'location_city': location.location_city, 'location_meta': location.location_meta}
    return jsonify(location_data)

@app.route('/api/v1/location/<location_id>', methods=['PUT'])
def update_location(location_id):
    data = request.get_json()
    location = Location.query.get(location_id)
    if not location:
        return make_response(jsonify({"error": "Location not found"}), 404)
    location.location_name = data.get('location_name', location.location_name)
    location.location_country = data.get('location_country', location.location_country)
    location.location_city = data.get('location_city', location.location_city)
    location.location_meta = data.get('location_meta', location.location_meta)
    db.session.commit()
    return jsonify({"message": "Location updated successfully"})

@app.route('/api/v1/location/<location_id>', methods=['DELETE'])
def delete_location(location_id):
    location = Location.query.get(location_id)
    if not location:
        return make_response(jsonify({"error": "Location not found"}), 404)
    db.session.delete(location)
    db.session.commit()
    return jsonify({"message": "Location deleted successfully"})

@app.route('/api/v1/admin/sensor', methods=['POST'])
def create_sensor():
    data = request.get_json()
    location_id = data.get('location_id')
    location = Location.query.get(location_id)
    if not location:
        return make_response(jsonify({"error": "Location not found"}), 404)
    
    sensor_name = data.get('sensor_name')
    sensor_category = data.get('sensor_category')
    sensor_meta = data.get('sensor_meta')
    sensor_api_key = str(uuid.uuid4())
    
    new_sensor = Sensor(location_id=location_id, sensor_name=sensor_name, sensor_category=sensor_category, sensor_meta=sensor_meta, sensor_api_key=sensor_api_key)
    db.session.add(new_sensor)
    db.session.commit()
    
    return make_response(jsonify({"message": "Sensor created successfully", "sensor_api_key": sensor_api_key}), 201)

@app.route('/api/v1/sensors', methods=['GET'])
def get_sensors():
    sensors = Sensor.query.all()
    output = []
    for sensor in sensors:
        sensor_data = {'id': sensor.id, 'location_id': sensor.location_id, 'sensor_name': sensor.sensor_name,
                       'sensor_category': sensor.sensor_category, 'sensor_meta': sensor.sensor_meta, 'sensor_api_key': sensor.sensor_api_key}
        output.append(sensor_data)
    return jsonify({'sensors': output})

@app.route('/api/v1/sensor/<sensor_id>', methods=['GET'])
def get_sensor(sensor_id):
    sensor = Sensor.query.get(sensor_id)
    if not sensor:
        return make_response(jsonify({"error": "Sensor not found"}), 404)
    sensor_data = {'id': sensor.id, 'location_id': sensor.location_id, 'sensor_name': sensor.sensor_name,
                   'sensor_category': sensor.sensor_category, 'sensor_meta': sensor.sensor_meta, 'sensor_api_key': sensor.sensor_api_key}
    return jsonify(sensor_data)

@app.route('/api/v1/sensor/<sensor_id>', methods=['PUT'])
def update_sensor(sensor_id):
    data = request.get_json()
    sensor = Sensor.query.get(sensor_id)
    if not sensor:
        return make_response(jsonify({"error": "Sensor not found"}), 404)
    sensor.sensor_name = data.get('sensor_name', sensor.sensor_name)
    sensor.sensor_category = data.get('sensor_category', sensor.sensor_category)
    sensor.sensor_meta = data.get('sensor_meta', sensor.sensor_meta)
    db.session.commit()
    return jsonify({"message": "Sensor updated successfully"})

@app.route('/api/v1/sensor/<sensor_id>', methods=['DELETE'])
def delete_sensor(sensor_id):
    sensor = Sensor.query.get(sensor_id)
    if not sensor:
        return make_response(jsonify({"error": "Sensor not found"}), 404)
    db.session.delete(sensor)
    db.session.commit()
    return jsonify({"message": "Sensor deleted successfully"})

@app.route('/api/v1/sensor_data', methods=['POST'])
def insert_sensor_data():
    data = request.get_json()
    sensor_api_key = data.get('api_key')
    sensor = Sensor.query.filter_by(sensor_api_key=sensor_api_key).first()
    if not sensor:
        return make_response(jsonify({"error": "Invalid sensor API key"}), 400)
    
    json_data = data.get('json_data')
    if not json_data or not isinstance(json_data, list):
        return make_response(jsonify({"error": "Invalid data format"}), 400)
    
    for entry in json_data:
        new_sensor_data = SensorData(sensor_id=sensor.id, data=entry)
        db.session.add(new_sensor_data)
    
    db.session.commit()
    
    return make_response(jsonify({"message": "Sensor data inserted successfully"}), 201)

@app.route('/api/v1/sensor_data', methods=['GET'])
def get_sensor_data():
    company_api_key = request.args.get('company_api_key')
    company = Company.query.filter_by(company_api_key=company_api_key).first()
    if not company:
        return make_response(jsonify({"error": "Invalid company API key"}), 400)
    
    from_time = request.args.get('from')
    to_time = request.args.get('to')
    sensor_ids = request.args.getlist('sensor_id')
    
    if not from_time or not to_time or not sensor_ids:
        return make_response(jsonify({"error": "Missing parameters"}), 400)
    
    from_time = datetime.datetime.fromtimestamp(int(from_time))
    to_time = datetime.datetime.fromtimestamp(int(to_time))
    
    sensor_data = SensorData.query.filter(SensorData.sensor_id.in_(sensor_ids), SensorData.timestamp >= from_time, SensorData.timestamp <= to_time).all()
    
    output = []
    for data in sensor_data:
        output.append({'sensor_id': data.sensor_id, 'timestamp': data.timestamp, 'data': data.data})
    
    return jsonify({'sensor_data': output})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001)