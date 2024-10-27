from flask import Blueprint, jsonify, request
from ..repositories.room_repository import (
    db_available_room_of_type,
    db_get_room,
    db_get_rooms,
    db_update_room_availability,
)

# Blueprint for room routes
room_routes = Blueprint('rooms', __name__)

# GET all rooms
@room_routes.route('', methods=['GET'])
def get_rooms():
    try:
        rooms = db_get_rooms()
        return jsonify(rooms), 200 if rooms else 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET specific room by id
@room_routes.route('/<int:room_id>', methods=['GET'])
def get_room(room_id):
    try:
        room = db_get_room(room_id)
        return jsonify(room), 200 if room else 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PATCH update room availability
@room_routes.route('/<int:room_id>/availability', methods=['PATCH'])
def update_room_availability(room_id):
    data = request.get_json()
    availability = data.get('availability')

    # Check if availability is present and valid
    if availability is None or not isinstance(availability, int):
        return jsonify({"error": "Invalid or missing field: availability"}), 400

    try:
        db_update_room_availability(room_id, availability)
        return jsonify({"message": "Room availability updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# GET first available room of specified type
@room_routes.route('/<int:room_type_id>/available', methods=['GET'])
def available_room_of_type(room_type_id):
    try:
        room_id = db_available_room_of_type(room_type_id)
        return jsonify({"room_id": room_id}), 200 if room_id else 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
