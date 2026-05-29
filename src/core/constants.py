BASE_URL = "https://data.gov.sg/api/action/datastore_search"
LIMIT = 10000

GOOGLE_MAPS_PLACES_URL = "https://places.googleapis.com/v1/places:searchText"
GOOGLE_MAPS_GEOCODING_URL = "https://maps.googleapis.com/maps/api/geocode/json"


PRIMARY_TYPES = {
    "subway_station": 0,
    "transit_station": 1,
    "train_station": 2,
    "transportation_service": 3,
    "light_rail_station": 4,
    "museum": 5,
}

STREET_NAME_ABB = {
    "Ave": "Avenue",
    "Bt": "Bukit",
    "Cl": "Close",
    "Cres": "Crescent",
    "Ctr": "Centre",
    "Ctrl": "Central",
    "C'Wealth": "Commonwealth",
    "Dr": "Drive",
    "Gdns": "Gardens",
    "Hts": "Heights",
    "Jln": "Jalan",
    "Kg": "Kampong",
    "Lor": "Lorong",
    "Mkt": "Market",
    "Nth": "North",
    "Pk": "Park",
    "Pl": "Place",
    "Rd": "Road",
    "St.": "Saint",
    "Sth": "South",
    "St": "Street",
    "Ter": "Terrace",
    "Tg": "Tanjong",
    "Upp": "Upper",
}
