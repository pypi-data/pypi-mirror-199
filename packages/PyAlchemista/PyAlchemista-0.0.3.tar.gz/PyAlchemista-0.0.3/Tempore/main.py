
import math
import datetime
import calendar


class Dates:
    def __init__(self, data):
        self.__dict__ = data
   


def juliandate(now):
    """
    :param now: preferably inputted as `datetime.datetime.now()`
    :return: Julian date
    """
    y = now.year  # year
    m = now.month  # month
    d = now.day  # day
    if m == 1 or m == 2:  # add 12 to the month -1 from the year
        y = y - 1  # -1 from the year
        m = m + 12  # add 1
    A = math.floor(y / 100)
    B = 2 - A + math.floor(A / 4)
    C = math.floor(365.25 * y)
    D = math.floor(30.6001 * (m + 1))
    return B + C + D + d + 1720994.5  # return Julian Date


def planetMeanAnomaly(planet):
    """
    :param planet: An str that contains the planet's name
    :return: the planet's mean anomaly
    """
    planet = planet.lower()
    m01 = {"mercury": [174.7948, 4.09233445],
           "venus": [50.4161, 1.60213034],
           "earth": [357.5291, 0.98560028],
           'mars': [19.3730, 0.52402068],
           'jupiter': [20.0202, 0.08308529],
           'saturn': [317.0207, 0.03344414],
           'uranus': [141.0498, 0.01172834],
           'neptune': [256.2250, 0.00598103],
           'pluto': [14.882, 0.00396]
           }
    j = juliandate(datetime.datetime.now())
    m_list = m01[planet]
    m0 = m_list[0]
    m1 = m_list[1]
    m = (m0 + m1 * (j - 2451545)) % 360
    return m


def planetEquationOfCenter(planet):
    """
    :param planet: an str that contains the planet's name (pluto is supported)
    :return: the planet's equation of center
    """
    """
    The orbits of the planets are not perfect circles but rather ellipses, so the speed of the planet in its orbit 
    varies,and therefore the apparent speed of the Sun along the ecliptic also varies throughout the planet's year. This
    correction factor is called the equation of center
    """
    c_dict = {
        "mercury": [23.4400, 2.9818, 0.5255, 0.1058, 0.0241, 0.0055],  # 0.0026 is the maximum error
        "venus": [0.7758, 0.0033, 0, 0, 0, 0],  # 0.0000 is the maximum error
        "earth": [1.9148, 0.0200, 0.0003, 0, 0, 0],  # 0.0000 is the maximum error
        "mars": [10.6912, 0.6228, 0.0503, 0.0046, 0.0005, 0],  # 0.0001 is the maximum error
        "jupiter": [5.5549, 0.1683, 0.0071, 0.0003, 0, 0],  # 0.0001 is the maximum error
        "saturn": [6.3585, 0.2204, 0.0106, 0.0006, 0, 0],  # 0.0001 is the maximum error
        "uranus": [5.3042, 0.1534, 0.0062, 0.0003, 0, 0],  # 0.0001 is the maximum error
        "neptune": [1.0302, 0.0058, 0, 0, 0, 0],  # 0.0001 is the maximum error
        "pluto": [28.3150, 4.3408, 0.9214, 0.2235, 0.0627, 0.0174]  # 0.0096 is the maximum error
    }
    # the formula used is from https://www.aa.quae.nl/en/reken/zonpositie.html#10
    # c = c1 * sin(m) + c2 * sin(2m) + c3 * sin(3m) + c4 * sin(4m) + c5 * sin(5m) + c6 * sin(6m)

    if planet.lower() in c_dict.keys():
        c = c_dict[planet.lower()]
    else:
        raise ValueError("planet is invalid")
    m = planetMeanAnomaly(planet.lower())
    center_eq = c[0] * math.sin(m) + c[1] * math.sin(2 * m) + c[2] * math.sin(3 * m) + c[3] * math.sin(4 * m) + \
                c[4] * math.sin(5 * m) + c[5] * math.sin(6 * m)
    return center_eq


def planetTrueAnomaly(planet):
    m = planetMeanAnomaly(planet)  # this is the mean anomaly of the planet
    c = planetEquationOfCenter(planet)  # this is the eq of center (correction factor)
    return m + c  # corrected anomaly


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

