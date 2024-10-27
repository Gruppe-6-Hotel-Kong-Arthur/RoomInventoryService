from flask import Flask, jsonify, request
from repositories.initialize import init_db
from repositories.room_repository import (
    db_available_room_of_type,
    db_get_room,
    db_get_rooms,
    db_update_room_availability,
)
from repositories.room_type_repository import (
    db_add_room_type,
    db_get_room_type,
    db_get_room_types,
    db_get_room_types_with_availability,
    db_update_room_type_price,
)

# Initializes Flask app
app = Flask(__name__)

# Retrieves all room types
@app.route('/api/v1/room_types', methods=['GET'])
def get_room_types():
    try:
        room_types = db_get_room_types()
    except Exception as e:        
        return jsonify({"error": str(e)}), 500

    if room_types:
        return jsonify(room_types)
    return jsonify({"error": "No room types found"}), 404

# Retrieves all room types with availability
@app.route('/api/v1/room_types/availability', methods=['GET'])
def get_room_types_with_availability():
    try:
        room_types = db_get_room_types_with_availability()
    except Exception as e:        
        return jsonify({"error": str(e)}), 500

    if room_types:
        return jsonify(room_types)
    return jsonify({"error": "No room types found"}), 404

# Retrieves specific room type by id
@app.route('/api/v1/room_types/<int:room_type_id>', methods=['GET'])
def get_room_type(room_type_id):
    try:
        room_type = db_get_room_type(room_type_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if room_type:
        return jsonify(room_type)
    return jsonify({"error": "Room type not found"}), 404

# Add new room type by name and base price
@app.route('/api/v1/room_types', methods=['POST'])
def add_room_type():
    data = request.get_json()
    required_fields = ['type_name', 'base_price', 'max_count']
    
    # Check if required fields are provided and are valid
    if not all(field in data for field in required_fields) or not isinstance(data['base_price'], (int, float)):
        return jsonify({"error": "Invalid or missing field"}), 400

    # Add room type and return success message
    try:
        db_add_room_type(data['type_name'], data['base_price'], data['max_count'])
        return jsonify({"message": "Room type added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Updates/Patches room type price
@app.route('/api/v1/room_types/<int:room_type_id>/price', methods=['PATCH'])
def update_room_type_price(room_type_id):
    data = request.get_json()
    base_price = data.get('base_price')
    
    # Validate base_price and room_type_id
    if base_price is None or not isinstance(base_price, (int, float)) or not isinstance(room_type_id, int):
        return jsonify({"error": "Invalid or missing field: base_price or room_type_id"}), 400

    # Update room type price and return success message or error
    try:
        db_update_room_type_price(room_type_id, float(base_price))
        return jsonify({"message": "Room type price updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Retrieves all rooms
@app.route('/api/v1/rooms', methods=['GET'])
def get_rooms():
    try:
        rooms = db_get_rooms()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    if rooms:
        return jsonify(rooms)
    return jsonify({"error": "No rooms found"}), 404

# Retrieves specific room by id
@app.route('/api/v1/rooms/<int:room_id>', methods=['GET'])
def get_room(room_id):
    # Get room by id and return room data or error
    try:
        room = db_get_room(room_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    if room:
        return jsonify(room)
    return jsonify({"error": "Room not found"}), 404

# Updates/Patches room availability by id
@app.route('/api/v1/rooms/<int:room_id>/availability', methods=['PATCH'])
def update_room_availability(room_id):
    data = request.get_json()
    availability = data.get('availability')

    # Check if availability is provided and is a valid integer
    if availability is None or not isinstance(availability, int) or not isinstance(room_id, int):
        return jsonify({"error": "Invalid or missing field: availability or room_id"}), 400
    
    # Update room availability and return success message or error
    try:
        db_update_room_availability(room_id, availability)
        return jsonify({"message": "Room availability updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Retrieves first available room of specified room type
@app.route('/api/v1/rooms/<int:room_type_id>/available', methods=['GET'])
def available_room_of_type(room_type_id):
    # Check if room_type_id is provided and is a valid integer
    if not room_type_id or not isinstance(room_type_id, int):
        return jsonify({"error": "Invalid room_type_id or missing field"}), 400

    # Get first available room of specified type
    try:
        room_id = db_available_room_of_type(room_type_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

# Initializes database and runs Flask app on port 5002
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5002, debug=True)