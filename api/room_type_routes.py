from flask import Blueprint, jsonify, request
from repositories.room_type_repository import (
    db_add_room_type,
    db_get_room_type,
    db_get_room_types,
    db_get_room_types_with_availability,
    db_update_room_type_price,
)

room_type_routes = Blueprint('room_types', __name__)

@room_type_routes.route('', methods=['GET'])
def get_room_types():
    try:
        room_types = db_get_room_types()
        return jsonify(room_types), 200 if room_types else 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@room_type_routes.route('/availability', methods=['GET'])
def get_room_types_with_availability():
    try:
        room_types = db_get_room_types_with_availability()
        return jsonify(room_types), 200 if room_types else 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@room_type_routes.route('/<int:room_type_id>', methods=['GET'])
def get_room_type(room_type_id):
    try:
        room_type = db_get_room_type(room_type_id)
        return jsonify(room_type), 200 if room_type else 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@room_type_routes.route('', methods=['POST'])
def add_room_type():
    data = request.get_json()
    required_fields = ['type_name', 'base_price', 'max_count']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Invalid or missing field"}), 400

    try:
        db_add_room_type(data['type_name'], data['base_price'], data['max_count'])
        return jsonify({"message": "Room type added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@room_type_routes.route('/<int:room_type_id>/price', methods=['PATCH'])
def update_room_type_price(room_type_id):
    data = request.get_json()
    base_price = data.get('base_price')
    
    if base_price is None or not isinstance(base_price, (int, float)):
        return jsonify({"error": "Invalid or missing field: base_price"}), 400

    try:
        db_update_room_type_price(room_type_id, base_price)
        return jsonify({"message": "Room type price updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
