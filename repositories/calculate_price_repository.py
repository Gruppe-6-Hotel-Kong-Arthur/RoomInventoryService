from database.connection import create_connection
from datetime import timedelta
from repositories.room_type_repository import db_get_room_base_price

# Fetch season multiplier based on dates (a date can belong to multiple seasons)
def _db_get_season_multiplier(date):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute('''
        SELECT multiplier FROM Seasons
        INNER JOIN SeasonDates ON Seasons.id = SeasonDates.season_id
        WHERE start_date <= ? AND end_date >= ?
    ''', (date, date))

    result = cursor.fetchone()
    connection.close()
    
    return result['multiplier'] if result else 1 # Default multiplier is 1 

# Calculate total price for stay duration (a stay can span multiple seasons)
def db_calculate_total_price(room_type_id, start_date, end_date):
    base_price = db_get_room_base_price(room_type_id)
    total_price = 0
    
    # Iterate over each date from start_date to end_date and calculate price per day and add to total_price 
    iterate_date = start_date
    while iterate_date <= end_date:
        multiplier = _db_get_season_multiplier(iterate_date)
        total_price += base_price * multiplier
        iterate_date += timedelta(days=1)
    
    return total_price if total_price else None
