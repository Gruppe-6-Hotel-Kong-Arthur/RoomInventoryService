from .connection import create_connection

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
