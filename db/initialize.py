import sqlite3
import pandas as pd
import os
from .connection import create_connection
from .config import BASE_PRICES, SEASONS

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

# Initializes database with tables and data
def init_db():
    _create_tables()

    # If data does not exist in database, insert base data and read CSV data
    if not _check_data_exists():
        _insert_season_multiplier_data()
        _insert_base_data()
        _read_csv_data()
    print("Database initialized successfully.")