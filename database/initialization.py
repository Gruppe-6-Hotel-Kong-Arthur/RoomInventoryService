import pandas as pd
import os
from database.connection import create_connection
from database.constants import BASE_PRICES, SEASONS, SEASON_DATES, ROOM_COUNTS

# Initializes database with tables and data
def init_db():
    _create_tables()

    # If data does not exist in database, insert base data and read CSV data
    if not _check_data_exists():
        _insert_season_multiplier_data()
        _insert_room_type_data()
        _insert_season_dates()
        _read_csv_data()

    print("Database initialized successfully.")

# Creates initial database tables
def _create_tables():
    try:

        connection = create_connection()
        cursor = connection.cursor()

        # Create RoomTypes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS RoomTypes (
                id INTEGER PRIMARY KEY,
                type_name TEXT NOT NULL UNIQUE,
                base_price REAL NOT NULL CHECK(base_price >= 0),
                max_count INTEGER NOT NULL CHECK(max_count > 0)
            )
        """)

        # Create index on type_name for efficient lookups in RoomTypes table
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS roomtypes_idx_type_name ON RoomTypes(type_name)
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

        # Create index on room_type_id for efficient joins in Rooms table
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS rooms_idx_room_type_id ON Rooms(room_type_id)
        """)

        # Create index on availability for efficient filtering in Rooms table
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS rooms_idx_availability ON Rooms(availability)
        """)

        # Create Seasons table 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Seasons (
                id INTEGER PRIMARY KEY,
                season_type TEXT NOT NULL UNIQUE,
                multiplier REAL NOT NULL CHECK(multiplier >= 0)
            )
        """)

        # Create index on season_type for efficient lookups in Seasons table
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS seasons_idx_season_type ON Seasons(season_type)
        """)

        # Create index on multiplier for efficient filtering in Seasons table
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS seasons_idx_multiplier ON Seasons(multiplier)
        """)

        # Create SeasonDates table (Unique constraint to prevent overlapping dates)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS SeasonDates (
                id INTEGER PRIMARY KEY,
                season_id INTEGER NOT NULL,
                start_date DATE NOT NULL CHECK(start_date >= DATE('now')), 
                end_date DATE NOT NULL CHECK(end_date >= start_date),
                FOREIGN KEY (season_id) REFERENCES Seasons(id),
                UNIQUE (season_id, start_date, end_date)
            )
        ''')

        # Create index on season_id for efficient joins in SeasonDates table
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS seasondates_idx_season_id ON SeasonDates(season_id)
        """)
    except Exception as e:
        print(f"Error creating tables: {e}")
        
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

# Insert base room type name, price and max_count with BASE_PRICES and ROOM_COUNTS into RoomTypes table
def _insert_room_type_data():
    connection = create_connection()
    cursor = connection.cursor()
    
    for type_name, base_price in BASE_PRICES.items():
        max_count = ROOM_COUNTS.get(type_name, 0)
        
        cursor.execute("""
            INSERT INTO RoomTypes (type_name, base_price, max_count) 
            VALUES (?, ?, ?)
        """, (type_name, base_price, max_count))
            
    connection.commit()
    connection.close()

# Insert season multiplier data with SEASONS into the Seasons table
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

# Insert season dates into SeasonDates table
def _insert_season_dates():
    connection = create_connection()
    cursor = connection.cursor()
    
    # Insert season dates using the SEASON_DATES constant
    cursor.executemany("""
        INSERT INTO SeasonDates (season_id, start_date, end_date) VALUES (?, ?, ?)
    """, SEASON_DATES)
    
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

    # Dictionary to keep track of the number of rooms inserted for each type
    room_counts = {type_name: 0 for type_name in ROOM_COUNTS.keys()}

    # Iterate over each row in the CSV file and insert the room type into the RoomTypes table
    for _, row in data.iterrows():
        room_type_name = row['Room Type']
        
        # Check if room type already exists in the RoomTypes table
        cursor.execute("SELECT id FROM RoomTypes WHERE type_name = ?", 
                       (room_type_name,))
        room_type = cursor.fetchone()
        
        # If room type exists, insert room data into Rooms table
        if room_type:
            room_type_id = room_type['id']
            
            # Increment the count for this room type
            room_counts[room_type_name] += 1
            
            # Calculate availability based on total_count
            total_count = ROOM_COUNTS[room_type_name]
            availability = 1 if room_counts[room_type_name] <= int(total_count * 0.8) else 0
            
            # Insert the room with the calculated availability
            cursor.execute("""
                INSERT INTO Rooms (room_type_id, availability) 
                VALUES (?, ?)
            """, (room_type_id, availability))

    connection.commit()
    connection.close()
