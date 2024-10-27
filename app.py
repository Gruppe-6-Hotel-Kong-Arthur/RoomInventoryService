from flask import Flask, jsonify, request
from db.initialize import init_db
from db.room_repository import (
    db_available_room_of_type,
    db_get_room,
    db_get_rooms,
    db_update_room_availability,
)
from db.room_type_repository import (
    db_add_room_type,
    db_get_room_type,
    db_get_room_types,
    db_update_room_type_price,
)

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
@app.route('/api/v1/room_types/<int:id>', methods=['GET'])
def get_room_type(id):
    room_type = db_get_room_type(id)
    if room_type:
        return jsonify(room_type)
    return jsonify({"error": "Room type not found"}), 404

# Add new room type by name and base price
@app.route('/api/v1/room_types', methods=['POST'])
def add_room_type():
    data = request.get_json()
    required_fields = ['type_name', 'base_price']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
        
    db_add_room_type(data['type_name'], float(data['base_price']))
    return jsonify({"message": "Room type added successfully"}), 201

# Updates/Patches room type price by id
@app.route('/api/v1/room_types/<int:id>/price', methods=['PATCH'])
def update_room_type_price(id):
    data = request.get_json()

    # Check if base_price is provided and is a valid number
    if 'base_price' not in data or not isinstance(data['base_price'], (int, float)):
        return jsonify({"error": "Invalid base_price or missing field"}), 400

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

# Retrieves first available room of specified type
@app.route('/api/v1/rooms/<int:room_type_id>/available', methods=['GET'])
def available_room_of_type(room_type_id):

    # Check if room_type_id is provided and is a valid integer
    if not room_type_id or not isinstance(room_type_id, int):
        return jsonify({"error": "Invalid room_type_id or missing field"}), 400

    room_id = db_available_room_of_type(room_type_id)

    # Return room_id if available, otherwise return error
    if room_id:
        return jsonify({"room_id": room_id})
    return jsonify({"error": "No available rooms found"}), 404

# ------------------------------ Error Handlers & Main ------------------------------ #

# Error handler for 404 Not Found
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

# Error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Initializes database and runs app
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5002, debug=True)