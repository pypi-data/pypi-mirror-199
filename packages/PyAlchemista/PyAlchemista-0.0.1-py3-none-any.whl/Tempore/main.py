
import math
import datetime
import calendar


def astroNorthernSeasonDates(year):
    # Calculate the spring equinox
    spring_equinox = (datetime.datetime(year, 3, 20, 21, 58) + datetime.timedelta(days=calendar.isleap(year))). \
        strftime("%h %d:%H:%S, %Y")
    # Calculate the summer solstice
    summer_solstice = (datetime.datetime(year, 6, 21, 10, 31) + datetime.timedelta(days=calendar.isleap(year))). \
        strftime("%h %d:%H:%S, %Y")
    # Calculate the autumnal equinox
    autumnal_equinox = (datetime.datetime(year, 9, 22, 19, 21) + datetime.timedelta(days=calendar.isleap(year))). \
        strftime("%h %d:%H:%S, %Y")
    # Calculate the winter solstice
    winter_solstice = (datetime.datetime(year, 12, 21, 15, 59) + datetime.timedelta(days=calendar.isleap(year))). \
        strftime("%h %d:%H:%S, %Y")

    # Return a dictionary of the astronomical seasons
    return Dates({
        'spring': spring_equinox,
        'summer': summer_solstice,
        'autumn': autumnal_equinox,
        'winter': winter_solstice
    })


def astroSouthernSeasonDates(year):
    # Calculate the autumnal equinox for the Southern Hemisphere
    autumnal_equinox = (datetime.datetime(year, 3, 20, 21, 58) + datetime.timedelta(days=calendar.isleap(year))). \
        strftime("%h %d:%H:%S, %Y")
    # Calculate the winter solstice for the Southern Hemisphere
    winter_solstice = (datetime.datetime(year, 6, 21, 10, 31) + datetime.timedelta(days=calendar.isleap(year))). \
        strftime("%h %d:%H:%S, %Y")
    # Calculate the spring equinox for the Southern Hemisphere
    spring_equinox = (datetime.datetime(year, 9, 22, 19, 21) + datetime.timedelta(days=calendar.isleap(year))). \
        strftime("%h %d:%H:%S, %Y")
    # Calculate the summer solstice for the Southern Hemisphere
    summer_solstice = (datetime.datetime(year, 12, 21, 15, 59) + datetime.timedelta(days=calendar.isleap(year))). \
        strftime("%h %d:%H:%S, %Y")

    # Return a dictionary of the astronomical seasons
    return Dates({
        'autumn': autumnal_equinox,
        'winter': winter_solstice,
        'spring': spring_equinox,
        'summer': summer_solstice,
    })


LUNAR_MONTH = 29.530588853


def get_lunar_age(date=datetime.date.today()):
    percent = get_lunar_age_percent(date)
    age = percent * LUNAR_MONTH
    return age


def get_lunar_age_percent(date=datetime.date.today()):
    julian_date = juliandate(date)
    return normalize((julian_date - 2451550.1) / LUNAR_MONTH)


def normalize(value):
    value = value - int(value)
    if value < 0:
        value = value + 1
    return value


def getLunarPhase(date=datetime.datetime.now()):
    age = get_lunar_age(date)
    if age < 1.84566:
        return "New"
    elif age < 5.53699:
        return "Waxing Crescent"
    elif age < 9.22831:
        return "First Quarter"
    elif age < 12.91963:
        return "Waxing Gibbous"
    elif age < 16.61096:
        return "Full"
    elif age < 20.30228:
        return "Waning Gibbous"
    elif age < 23.99361:
        return "Last Quarter"
    elif age < 27.68493:
        return "Waning Crescent"
    return "New"

