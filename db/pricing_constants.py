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
