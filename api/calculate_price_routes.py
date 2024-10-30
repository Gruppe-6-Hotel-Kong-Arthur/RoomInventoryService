from flask import Blueprint, jsonify, request
from repositories.calculate_price_repository import db_calculate_total_price, db_get_season_name
from repositories.room_type_repository import db_get_room_type
from datetime import datetime

calculate_price_routes = Blueprint('calculate_price_routes', __name__)

# GET total price for stay duration by room type and start/end dates
# Example: /api/v1/calculate_price/1?start_date=2024-11-01&end_date=2024-11-03 (YYYY-MM-DD)
@calculate_price_routes.route('/<int:room_type_id>', methods=['GET'])
def get_total_price(room_type_id):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Check if room type exists
    if db_get_room_type(room_type_id) is None:
        return jsonify({"error": "Room type not found"}), 404
    
    # Check if start_date and end_date are present and valid
    if not start_date or not end_date:
        return jsonify({"error": "Missing field: start_date or end_date as query parameters"}), 400
    
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    try:
        season = db_get_season_name(start_date)
        total_price = db_calculate_total_price(room_type_id, start_date, end_date)

        response = {
            "price": total_price,
            "season": season
        }
        
        return jsonify(response), 200 if response else 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
