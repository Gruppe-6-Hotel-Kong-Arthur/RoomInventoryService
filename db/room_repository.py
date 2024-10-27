from .connection import create_connection

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
