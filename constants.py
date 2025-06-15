# constants.py
ROLES = ['admin', 'staff', 'customer']

US_STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA',
    'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
    'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

COLORS = {
    'color_1': '#18AEC9',
    'color_2': '#EBCE0F',
    "sidebar": "#1E90FF",
    "white": "#FFFFFF",
    "highlight": "#FFA500"
}

# List of car makes
CAR_MAKES = [
    "Toyota", "Ford", "Chevrolet", "Honda", "Nissan", "Jeep", "Hyundai", "Kia", "Subaru", "Tesla",
    "BMW", "Mercedes-Benz", "Volkswagen", "Audi", "Lexus", "Mazda", "Chrysler", "Dodge", "Ram", "GMC"
]

# Dictionary mapping car makes to their models
CAR_MODELS = {
    "Toyota": ["Camry", "Corolla", "RAV4", "Prius", "Highlander", "Tacoma", "Sienna"],
    "Ford": ["F-150", "Mustang", "Explorer", "Escape", "Focus", "Fusion", "Edge"],
    "Chevrolet": ["Silverado", "Malibu", "Equinox", "Traverse", "Camaro", "Corvette", "Tahoe"],
    "Honda": ["Civic", "Accord", "CR-V", "Pilot", "Odyssey", "Fit", "HR-V"],
    "Nissan": ["Altima", "Sentra", "Rogue", "Pathfinder", "Murano", "Titan", "Leaf"],
    "Jeep": ["Wrangler", "Cherokee", "Grand Cherokee", "Compass", "Renegade"],
    "Hyundai": ["Tucson", "Santa Fe", "Elantra", "Sonata", "Kona", "Palisade"],
    "Kia": ["Telluride", "Sorento", "Sportage", "Optima", "Soul", "Forte"],
    "Subaru": ["Outback", "Forester", "Crosstrek", "Impreza", "Ascent", "WRX"],
    "Tesla": ["Model S", "Model 3", "Model X", "Model Y", "Cybertruck"],
    "BMW": ["3 Series", "5 Series", "X3", "X5", "7 Series", "i4"],
    "Mercedes-Benz": ["C-Class", "E-Class", "S-Class", "GLC", "GLE", "GLS"],
    "Volkswagen": ["Jetta", "Passat", "Tiguan", "Atlas", "Golf", "ID.4"],
    "Audi": ["A3", "A4", "A6", "Q5", "Q7", "e-tron"],
    "Lexus": ["RX", "NX", "ES", "IS", "GX", "LX"],
    "Mazda": ["CX-5", "CX-9", "Mazda3", "Mazda6", "MX-5 Miata"],
    "Chrysler": ["Pacifica", "300", "Voyager"],
    "Dodge": ["Charger", "Challenger", "Durango", "Journey"],
    "Ram": ["1500", "2500", "3500"],
    "GMC": ["Sierra", "Yukon", "Terrain", "Acadia", "Canyon"]
}