from ..database.connection import create_connection

# Retrieves all rooms with type information, excluding max_count
def db_get_rooms():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT Rooms.id, Rooms.room_type_id, Rooms.availability, RoomTypes.type_name, RoomTypes.base_price
        FROM Rooms
        INNER JOIN RoomTypes ON Rooms.room_type_id = RoomTypes.id
    """)
    result = [dict(row) for row in cursor.fetchall()]
    connection.close()
    return result

# Gets specific room by id with type information, excluding max_count
def db_get_room(id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT Rooms.id, Rooms.room_type_id, Rooms.availability, RoomTypes.type_name, RoomTypes.base_price
        FROM Rooms
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

# Returns first available room of specified type
def db_available_room_of_type(room_type_id):
    connection = create_connection()
    cursor = connection.cursor()

    # Select first available room of specified type
    cursor.execute("""
        SELECT id FROM Rooms 
        WHERE room_type_id = ? AND availability = 1
        LIMIT 1
    """, (room_type_id,))
    room = cursor.fetchone()

    connection.close()
    
    return room['id'] if room else None
