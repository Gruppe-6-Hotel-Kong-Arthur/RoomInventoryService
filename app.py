from flask import Flask, jsonify, request
from db.db import (
    init_db,
    db_get_room_types,
    db_get_room_type_by_id,
    db_add_room_type,
    db_get_available_rooms,
    db_add_room,
    db_get_room_by_id,
    db_get_all_rooms
)

app = Flask(__name__)

# Retrieve all room types from the database
@app.route('/api/v1/room-types', methods=['GET'])
def get_room_types():
    room_types = db_get_room_types()

    if room_types:
        return jsonify(room_types), 200
    return jsonify({"error": "No room types found"}), 404

# Retrieve a specific room type by ID
@app.route('/api/v1/room-types/<int:id>', methods=['GET'])
def get_room_type_by_id(id):
    room_type = db_get_room_type_by_id(id)

    if room_type:
        return jsonify(room_type), 200
    return jsonify({"error": "Room type not found"}), 404

# Retrieve a specific room by ID
@app.route('/api/v1/rooms/<int:id>', methods=['GET'])
def get_room_by_id(id):
    room = db_get_room_by_id(id)

    if room:
        return jsonify(room), 200
    return jsonify({"error": "Room not found"}), 404

# Retrieve all rooms from the database
@app.route('/api/v1/rooms', methods=['GET'])
def get_all_rooms():
    rooms = db_get_all_rooms()

    if rooms:
        return jsonify(rooms), 200
    return jsonify({"error": "No rooms found"}), 404

# Add a new room type to the database
@app.route('/api/v1/room-types', methods=['POST'])
def add_room_type():
    data = request.get_json()
    type_name = data.get('type_name')
    base_price = data.get('base_price')

    # Check if the required fields are present
    if not all([type_name, base_price]):
        return jsonify({"error": "Missing required fields"}), 400

    # Add room type to the database
    if db_add_room_type(type_name, base_price):
        return jsonify({"message": "Room type added successfully"}), 201
    
    return jsonify({"error": "Failed to add room type"}), 500

# Retrieve all available rooms from the database
@app.route('/api/v1/rooms', methods=['GET'])
def get_rooms():
    available_rooms = db_get_available_rooms()

    if available_rooms:
        return jsonify(available_rooms), 200
    return jsonify({"error": "No available rooms found"}), 404

# Add a new room to the database
@app.route('/api/v1/rooms', methods=['POST'])
def add_room():
    data = request.get_json()
    room_type_id = data.get('room_type_id')

    # Check if the required fields are present
    if not room_type_id:
        return jsonify({"error": "Missing required fields"}), 400
    
    # Add room to the database
    if db_add_room(room_type_id):
        return jsonify({"message": "Room added successfully"}), 201

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5002)
