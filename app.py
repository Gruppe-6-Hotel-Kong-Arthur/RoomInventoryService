from flask import Flask, jsonify, request
from db.initialize import init_db
from db.room_types import db_get_room_types, db_get_room_type, db_add_room_type, db_update_room_type_price
from db.rooms import db_get_rooms, db_get_room, db_update_room_availability

# Initializes Flask app
app = Flask(__name__)

# Retrieves all room types
@app.route('/api/v1/room_types', methods=['GET'])
def get_room_types():
    room_types = db_get_room_types()
    if room_types:
        return jsonify(room_types)
    return jsonify({"error": "No room types found"}), 404

# Retrieves specific room type by id
@app.route('/api/v1/room_type/<int:id>', methods=['GET'])
def get_room_type(id):
    room_type = db_get_room_type(id)
    if room_type:
        return jsonify(room_type)
    return jsonify({"error": "Room type not found"}), 404

# Add new room type by name and base price
@app.route('/api/v1/room_type', methods=['POST'])
def add_room_type():
    data = request.get_json()
    required_fields = ['type_name', 'base_price']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
        
    db_add_room_type(data['type_name'], float(data['base_price']))
    return jsonify({"message": "Room type added successfully"}), 201

# Updates/Patches room type price by id
@app.route('/api/v1/room_type/<int:id>/price', methods=['PATCH'])
def update_room_type_price(id):
    data = request.get_json()
    db_update_room_type_price(id, float(data['base_price']))
    return jsonify({"message": "Price updated successfully"}), 200

# Retrieves all rooms
@app.route('/api/v1/rooms', methods=['GET'])
def get_rooms():
    rooms = db_get_rooms()
    if rooms:
        return jsonify(rooms)
    return jsonify({"error": "No rooms found"}), 404

# Retrieves specific room by id
@app.route('/api/v1/rooms/<int:id>', methods=['GET'])
def get_room(id):
    room = db_get_room(id)
    if room:
        return jsonify(room)
    return jsonify({"error": "Room not found"}), 404

# Updates/Patches room availability by id
@app.route('/api/v1/rooms/<int:id>/availability', methods=['PATCH'])
def update_room_availability(id):
    data = request.get_json()
    db_update_room_availability(id, int(data['availability']))
    return jsonify({"message": "Room availability updated successfully"}), 200

# Initializes database and runs app
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5002, debug=True)