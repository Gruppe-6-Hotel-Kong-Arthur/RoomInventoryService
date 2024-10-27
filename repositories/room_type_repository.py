from database.connection import create_connection

# Gets all room types 
def db_get_room_types():
    connection = create_connection()
    cursor = connection.cursor()

    # Retrieve all room types from the RoomTypes table and order them by base price
    cursor.execute('SELECT * FROM RoomTypes ORDER BY base_price')
    result = [dict(row) for row in cursor.fetchall()]
    connection.close()
    return result

# Gets all room types with availability
def db_get_room_types_with_availability():
    connection = create_connection()
    cursor = connection.cursor()

    # Retrieve all room types from the RoomTypes table with max_count and available_count and order them by id
    cursor.execute("""
        SELECT RoomTypes.id, RoomTypes.type_name, RoomTypes.base_price, COUNT(Rooms.id) as available_count, RoomTypes.max_count
        FROM RoomTypes
        LEFT JOIN Rooms ON RoomTypes.id = Rooms.room_type_id AND Rooms.availability = 1
        GROUP BY RoomTypes.id
    """)
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

# Add new room type
def db_add_room_type(type_name, base_price, max_count):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO RoomTypes (type_name, base_price, max_count)
        VALUES (?, ?, ?)
    """, (type_name, base_price, max_count))
    connection.commit()
    connection.close()
    return True

# Updates room type price
def db_update_room_type_price(id, base_price):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('UPDATE RoomTypes SET base_price = ? WHERE id = ?', (base_price, id))
    connection.commit()
    connection.close()
    return True
