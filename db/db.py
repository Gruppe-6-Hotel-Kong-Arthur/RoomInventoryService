import sqlite3
import pandas as pd
import os

# Base room prices (in DKK) for each room type
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

# Season multipliers (LOW= 20% off, MID= normal season, HIGH= 20% more expensive)
SEASONS = {
    'LOW': 0.8,
    'MID': 1.0,
    'HIGH': 1.2
}

# Creates database connection with row factory
def create_connection():
    connection = sqlite3.connect('db/room_inventory.db')
    connection.row_factory = sqlite3.Row
    return connection

# Creates initial database tables
def _create_tables():
    connection = create_connection()
    cursor = connection.cursor()

    # Create RoomTypes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS RoomTypes (
            id INTEGER PRIMARY KEY,
            type_name TEXT NOT NULL UNIQUE,
            base_price REAL NOT NULL
        )
    """)

    # Create Rooms table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Rooms (
            id INTEGER PRIMARY KEY,
            room_type_id INTEGER NOT NULL,
            availability INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (room_type_id) REFERENCES RoomTypes(id)
        )
    """)

    # Create Seasons table 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Seasons (
            id INTEGER PRIMARY KEY,
            season_type TEXT NOT NULL,
            multiplier REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()

# Checks if initial data exists in database
def _check_data_exists():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) count FROM RoomTypes")
    result = cursor.fetchone()['count'] > 0
    connection.close()
    return result

# Iterate over the BASE_PRICES dictionary and insert each room type and its corresponding base price into the RoomTypes table.
def _insert_base_data():
    connection = create_connection()
    cursor = connection.cursor()
    
    for type_name, base_price in BASE_PRICES.items():
        cursor.execute("""
            INSERT INTO RoomTypes (type_name, base_price) 
            VALUES (?, ?)
        """, (type_name, base_price))
            
    connection.commit()
    connection.close()

# Iterate over the SEASONS dictionary and insert each season type and its corresponding multiplier into the Seasons table.
def _insert_season_multiplier_data():
    connection = create_connection()
    cursor = connection.cursor()
    
    for season_type, multiplier in SEASONS.items():
        cursor.execute("""
            INSERT INTO Seasons (season_type, multiplier) 
            VALUES (?, ?)
        """, (season_type, multiplier))
            
    connection.commit()
    connection.close()

# Reads and inserts room data from CSV
def _read_csv_data():
    # Read CSV file by specifying the CSV file path
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                           'csv/international_names_with_rooms_1000.csv')
    data = pd.read_csv(csv_path)
    
    connection = create_connection()
    cursor = connection.cursor()

    # Iterate over each row in the CSV file and insert the room type into the RoomTypes table
    for index, row in data.iterrows():
        room_type_name = row['Room Type']
        
        # Check if room type already exists in the RoomTypes table
        cursor.execute("SELECT id FROM RoomTypes WHERE type_name = ?", 
                      (room_type_name,))
        room_type = cursor.fetchone()
        
        # If room type does not exist, insert it into the RoomTypes table
        if room_type:
            cursor.execute("""
                INSERT INTO Rooms (room_type_id, availability) 
                VALUES (?, 1)
            """, (room_type['id'],))

    connection.commit()
    connection.close()

# Gets all room types 
def db_get_room_types():
    connection = create_connection()
    cursor = connection.cursor()

    # Retrieve all room types from the RoomTypes table and order them by base price
    cursor.execute('SELECT * FROM RoomTypes ORDER BY base_price')
    result = [dict(row) for row in cursor.fetchall()]
    connection.close()
    return result

# Gets specific room type by id
def db_get_room_type(id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM RoomTypes WHERE id = ?', (id,))
    result = cursor.fetchone()
    connection.close()
    return dict(result) if result else None

# Adds new room type
def db_add_room_type(type_name, base_price):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO RoomTypes (type_name, base_price) 
        VALUES (?, ?)
    """, (type_name, base_price))
    connection.commit()
    connection.close()
    return True

# Updates room type price
def db_update_room_type_price(id, base_price):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""UPDATE RoomTypes SET base_price = ? WHERE id = ?""", (base_price, id))
    connection.commit()
    connection.close()
    return True

# Retrieves all rooms along with their type information
def db_get_rooms():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * FROM Rooms
        INNER JOIN RoomTypes ON Rooms.room_type_id = RoomTypes.id
    """)
    result = [dict(row) for row in cursor.fetchall()]
    connection.close()
    return result

# Gets specific room with type info
def db_get_room(id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * FROM Rooms
        INNER JOIN RoomTypes ON Rooms.room_type_id = RoomTypes.id
        WHERE Rooms.id = ?
    """, (id,))
    result = cursor.fetchone()
    connection.close()
    return dict(result) if result else None

# Updates room availability
def db_update_room_availability(id, availability):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Rooms 
        SET availability = ?
        WHERE id = ?
    """, (availability, id))
    connection.commit()
    connection.close()
    return True

# Initializes database with tables and data
def init_db():
    _create_tables()

    # If data does not exist in database, insert base data and read CSV data
    if not _check_data_exists():
        _insert_season_multiplier_data()
        _insert_base_data()
        _read_csv_data()
    print("Database initialized successfully.")
