import sqlite3
import pandas as pd
import os

# Base prices for each room type
BASE_PRICES = {
    'Standard Single': 900,
    'Grand Lit': 1100,
    'Standard Double': 1200,
    'Superior Double': 1400,
    'Junior Suite': 1800,
    'Spa Executive': 2000,
    'Suite': 2500,
    'LOFT Suite': 3000,
}

# Seasonal multipliers
SEASONAL_MULTIPLIERS = {
    'LOW': 0.8,
    'MID': 1.0,
    'HIGH': 1.2,
}

# ===================================================================================

# Create or connect to SQLite database
def create_connection():
    connection = sqlite3.connect('db/room_inventory.db')
    connection.row_factory = sqlite3.Row  # Rows as dictionaries
    return connection

# Initialize database and create necessary tables
def init_db():
    create_tables()

    if not insert_base_room_types():
        print("Failed to insert base room types.")

    if not insert_seasonal_multipliers():
        print("Failed to insert seasonal multipliers.")

    if not read_data_from_csv():
        print("Failed to read data from CSV and populate Rooms table.")

    print("Database initialized successfully.")

# Create necessary tables for room inventory
def create_tables():
    connection = create_connection()
    cursor = connection.cursor()

    # Create RoomTypes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS RoomTypes (
            id INTEGER PRIMARY KEY,
            type_name VARCHAR(100) UNIQUE NOT NULL,
            base_price REAL NOT NULL CHECK(base_price > 0)
        )
    """)

    # Create Rooms table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Rooms (
            id INTEGER PRIMARY KEY,
            room_type_id INTEGER NOT NULL,
            available INTEGER CHECK(available IN (0, 1)) NOT NULL,
            FOREIGN KEY (room_type_id) REFERENCES RoomTypes(id)
        )
    """)

    # Create SeasonalMultiplier table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SeasonalMultiplier (
            id INTEGER PRIMARY KEY,
            season VARCHAR(10) NOT NULL UNIQUE,
            multiplier REAL NOT NULL CHECK(multiplier > 0)
        )
    """)

    connection.commit()
    connection.close()

# Populate RoomTypes table with base prices
def insert_base_room_types():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) AS count FROM RoomTypes")
    if cursor.fetchone()['count'] == 0:
        for type_name, base_price in BASE_PRICES.items():
            try:
                cursor.execute("INSERT INTO RoomTypes (type_name, base_price) VALUES (?, ?)", (type_name, base_price))
            except Exception as e:
                print(f"Error adding base room type '{type_name}': {e}")
                return False

    connection.commit()
    connection.close()
    return True  # Return True after successful execution

# Insert seasonal multipliers into the database
def insert_seasonal_multipliers():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) AS count FROM SeasonalMultiplier")
    if cursor.fetchone()['count'] == 0:
        for season, multiplier in SEASONAL_MULTIPLIERS.items():
            try:
                cursor.execute("INSERT INTO SeasonalMultiplier (season, multiplier) VALUES (?, ?)", (season, multiplier))
            except Exception as e:
                print(f"Error adding seasonal multiplier for '{season}': {e}")
                return False

    connection.commit()
    connection.close()
    return True  # Return True after successful execution

# Read data from CSV and populate the Rooms table
def read_data_from_csv():
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'csv/international_names_with_rooms_1000.csv')
    data = pd.read_csv(csv_path)

    connection = create_connection()
    cursor = connection.cursor()

    for _, row in data.iterrows():
        room_type_name = row['Room Type']

        cursor.execute("SELECT id FROM RoomTypes WHERE type_name = ?", (room_type_name,))
        room_type = cursor.fetchone()

        if room_type:
            room_type_id = room_type['id']
            try:
                cursor.execute("INSERT INTO Rooms (room_type_id, available) VALUES (?, 1)", (room_type_id,))
            except Exception as e:
                print(f"Error adding room for room type ID {room_type_id}: {e}")
                return False
        else:
            print(f"Room type '{room_type_name}' not found.")
            return False

    connection.commit()
    connection.close()
    return True  # Return True after successful execution

# ===================================================================================

# Retrieve all room types
def db_get_room_types():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM RoomTypes')

    guests = cursor.fetchall()
    connection.close()
    
    if guests:
        return [dict(guest) for guest in guests]
    else:
        return None

# Retrieve a specific room type by ID
def db_get_room_type_by_id(id):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM RoomTypes WHERE id = ?", (id,))

    room_type = cursor.fetchone()
    connection.close()

    if room_type:
        return dict(room_type)
    else:
        return None
    
# Add a new room type to the database
def db_add_room_type(type_name, base_price):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO RoomTypes (type_name, base_price) VALUES (?, ?)", (type_name, base_price))
        connection.commit()
        return True
    except Exception as e:
        print(f"Failed to add room type: {e}")
        return False
    finally:
        connection.close()

# Retrieve all available rooms TODO:ONLY SEND BASE PRICE
def db_get_available_rooms():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT Rooms.id, RoomTypes.type_name, RoomTypes.base_price, 
               CASE WHEN Rooms.available = 1 THEN 'True' ELSE 'False' END as available
        FROM Rooms
        INNER JOIN RoomTypes ON Rooms.room_type_id = RoomTypes.id
        WHERE Rooms.available = 1
    """)

    rooms = cursor.fetchall()
    connection.close()

    if rooms:
        return [dict(room) for room in rooms]
    else:
        return None

# Add a new room to the database
def db_add_room(room_type_id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO Rooms (room_type_id, available) VALUES (?, 1)", (room_type_id,))
        connection.commit()
        return True
    except Exception as e:
        print(f"Failed to add room: {e}")
        return False
    finally:
        connection.close()

# Retrieve all rooms
def db_get_all_rooms():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT Rooms.id, RoomTypes.type_name, RoomTypes.base_price, 
               CASE WHEN Rooms.available = 1 THEN 'True' ELSE 'False' END as available
        FROM Rooms
        INNER JOIN RoomTypes ON Rooms.room_type_id = RoomTypes.id
    """)

    rooms = cursor.fetchall()
    connection.close()

    if rooms:
        return [dict(room) for room in rooms]
    else:
        return

# Get a room by ID
def db_get_room_by_id(id):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT Rooms.id, RoomTypes.type_name, RoomTypes.base_price, 
               CASE WHEN Rooms.available = 1 THEN 'True' ELSE 'False' END as available
        FROM Rooms
        INNER JOIN RoomTypes ON Rooms.room_type_id = RoomTypes.id
        WHERE Rooms.id = ?
    """, (id,))

    room = cursor.fetchone()
    connection.close()

    if room:
        return dict(room)
    else:
        return None

# Execute the database initialization
init_db()
