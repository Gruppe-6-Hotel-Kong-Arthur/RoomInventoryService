from flask import Flask
from repositories.initialize import init_db
from api.room_routes import room_routes
from api.room_type_routes import room_type_routes

app = Flask(__name__)

# Register blueprints for modular endpoints
app.register_blueprint(room_routes, url_prefix='/api/v1/rooms')
app.register_blueprint(room_type_routes, url_prefix='/api/v1/room_types')

# Initialize the database
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5002, debug=True)
