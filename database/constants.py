# Base prices for different room types (in currency units, e.g., DKK)
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

# Seasonal price multipliers for adjusting room rates
SEASONS = {
    'LOW': 0.8,   # Low season multiplier (20% discount)
    'MID': 1.0,   # Mid season multiplier (normal price)
    'HIGH': 1.2    # High season multiplier (20% increase)
}

# Season dates with corresponding season IDs
SEASON_DATES = [
    (1, '2024-01-06', '2024-03-31'),  # LOW season (Winter)
    (2, '2024-04-01', '2024-06-14'),  # MID season (Spring)
    (3, '2024-06-15', '2024-08-31'),  # HIGH season (Summer)
    (2, '2024-09-01', '2024-10-31'),  # MID season (Early Fall)
    (2, '2024-12-01', '2024-12-14'),  # MID season (Pre-Christmas)
    (3, '2024-12-15', '2025-01-05'),  # HIGH season (Christmas/New Year)
    (1, '2024-11-01', '2024-11-30')   # LOW season (Late Fall)
]

# Room counts for each type (214 in total)
ROOM_COUNTS = {
    'Standard Single': 50,
    'Grand Lit': 50,
    'Standard Double': 40,
    'Superior Double': 25,
    'Junior Suite': 20,
    'Spa Executive': 15,
    'Suite': 10,
    'LOFT Suite': 4
}
