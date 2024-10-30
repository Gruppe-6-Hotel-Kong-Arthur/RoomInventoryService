from database.connection import create_connection
from datetime import timedelta, datetime
from repositories.room_type_repository import db_get_room_base_price

# Fetch season multiplier based on dates (a date can belong to multiple seasons)
def _db_get_season_multiplier(date):
    connection = create_connection()
    cursor = connection.cursor()

    # Format date properly for SQLite comparison
    formatted_date = date.strftime('%Y-%m-%d')

    cursor.execute('''
        SELECT multiplier FROM Seasons
        INNER JOIN SeasonDates ON Seasons.id = SeasonDates.season_id
        WHERE start_date <= ? AND end_date >= ?
    ''', (formatted_date, formatted_date))

    result = cursor.fetchone()
    connection.close()
    
    return result['multiplier'] if result else 1.0 # Default multiplier is 1 

# Calculate total price for stay duration (a stay can span multiple seasons)
def db_calculate_total_price(room_type_id, start_date, end_date):
    base_price = db_get_room_base_price(room_type_id)
    total_price = 0
    
    # Iterate over each date from start_date to end_date and calculate price per day and add to total_price 
    iterate_date = start_date
    while iterate_date <= end_date:
        multiplier = _db_get_season_multiplier(iterate_date)
        daily_price = base_price * multiplier
        total_price += daily_price
        iterate_date += timedelta(days=1)
    
    return total_price if total_price > 0 else None

# Get season by date
def db_get_season_by_date(date):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Convert input date to string in YYYY-MM-DD format (SQLite supports text comparisons)
        date_str = date if isinstance(date, str) else date.strftime("%Y-%m-%d")
        
        cursor.execute('''
            SELECT Seasons.id, Seasons.season_type, SeasonDates.start_date, SeasonDates.end_date
            FROM Seasons
            INNER JOIN SeasonDates ON Seasons.id = SeasonDates.season_id
            WHERE start_date <= ? AND end_date >= ?
        ''', (date_str, date_str))

        result = cursor.fetchone()
        
        # Close the connection
        connection.close()

        if not result:
            return None

        # Return result as a dictionary with clear keys
        return {
            "id": result["id"],
            "season_type": result["season_type"],
            "start_date": result["start_date"],
            "end_date": result["end_date"]
        }

    except Exception as e:
        print(e)
        return {"error": str(e)}


# Get season type by id
def db_get_season_by_id(id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute('''
            SELECT * FROM Seasons
            WHERE id = ?
        ''', (id,))

        result = cursor.fetchone()
        connection.close()

    except Exception as e:
        print(e)
    
    return dict(result) if result else None
