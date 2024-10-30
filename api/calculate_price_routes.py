from flask import Blueprint, jsonify, request
from datetime import datetime
from repositories.calculate_price_repository import db_calculate_total_price, db_get_season_by_id, db_get_season_by_date
from repositories.room_type_repository import db_get_room_type

calculate_price_routes = Blueprint('calculate_price_routes', __name__)

# GET Season name by id
@calculate_price_routes.route('/season_type/<int:season_id>', methods=['GET'])
def get_season_name(season_id):
    try:
        season = db_get_season_by_id(season_id)
        return jsonify(season), 200 if season else 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
        # Ensure the start and end dates are parsed correctly as datetime objects
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")

        season = db_get_season_by_date(start_date_dt)
        total_price = db_calculate_total_price(room_type_id, start_date_dt, end_date_dt)

        response = {
            "price": total_price,
            "season": season
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
