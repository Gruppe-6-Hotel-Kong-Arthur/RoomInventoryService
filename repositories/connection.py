import sqlite3

# Creates database connection with row factory
def create_connection():
    connection = sqlite3.connect('repositories/room_inventory.db')
    connection.row_factory = sqlite3.Row
    return connection