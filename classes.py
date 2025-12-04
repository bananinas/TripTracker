
#def get_holiday_types():
#    return [
#        {"value": "Beach holiday"},
#        {"value": "City break"},
#        {"value": "History & culture"},
#        {"value": "Nature & hiking"},
#        {"value": "Road trip"},
#        {"value": "Combination trip"},
#        {"value": "Other"},
#    ]

#def get_themes():
#    return [
#        {"value": "Couple"},
#        {"value": "Family"},
#        {"value": "Friends"},
#        {"value": "Solo"},
#        {"value": "Work trip"},
#        {"value": "Other"},
#   ]

import db

def get_holiday_types():
    return db.query("SELECT value FROM classes WHERE title='Holiday type' ORDER BY value", [])

def get_themes():
    return db.query("SELECT value FROM classes WHERE title='Theme' ORDER BY value", [])
