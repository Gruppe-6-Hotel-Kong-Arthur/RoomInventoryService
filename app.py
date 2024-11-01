from flask import Flask, jsonify
from database.initialization import init_db
from api.room_routes import room_routes
from api.room_type_routes import room_type_routes
from api.calculate_price_routes import calculate_price_routes

app = Flask(__name__)

# Register blueprints for modular endpoints
app.register_blueprint(room_routes, url_prefix='/api/v1/rooms')
app.register_blueprint(room_type_routes, url_prefix='/api/v1/room_types')
app.register_blueprint(calculate_price_routes, url_prefix='/api/v1/calculate_price')

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
    app.run(host='0.0.0.0', port=5002)
