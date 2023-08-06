import math
import datetime


class Sun:
    def __init__(self, data):
        self.__dict__ = data


class Moon:
    def __init__(self, data):
        self.__dict__ = data


class LST:
    def __init__(self, data):
        self.__dict__ = data


def getSunData(latitude: float, date=datetime.datetime.now()) -> Sun:
    """

    :param latitude: latitude of the user
    :param date: any date the user wishes
    :return: an object that contains solar information
    """

    if latitude > 90 or latitude < -90:
        raise ValueError("Latitude out of range (-90, 90)")

    """
    SOLAR DISTANCE (MILES)
    """
    lat = latitude
    now = date
    # Calculate the Julian date
    julian_date = 367 * now.year - int(7 * (now.year + int((now.month + 9) / 12)) / 4) + int(
        275 * now.month / 9) + now.day + 1721013.5 + now.hour / 24 + now.minute / 1440 + now.second / 86400
    # days since greenwich noon
    n = julian_date - 2451545
    # positions
    # g is mean anomaly
    g = 357.528 + 0.9856003 * n
    tmp = math.cos(g)
    temp_two = math.cos(2 * g)
    # solar distance is in astronomical units
    solar_distance = (1.00014 - 0.01671 * tmp - 0.00014 * temp_two)

    """
    DECLINATION
    """
    current_utc = datetime.datetime.utcnow()
    day_of_year = current_utc.timetuple().tm_yday
    solar_declination = -23.45 * math.cos(math.radians((360 / 365) * (day_of_year + 10)))

    """
    GEOMETRIC MEAN LONGITUDE
    """
    jd = julian_date
    # Calculate the Julian Century (JC) for the given JD
    jc = (jd - 2451545) / 36525
    # Calculate the Geometric Mean Longitude of the Sun (L0) in degrees
    l0 = 280.46646 + jc * (36000.76983 + jc * 0.0003032) % 360

    """
    GEOMETRIC MEAN ANOMALY
    """
    # Calculate the Geometric Mean Anomaly of the Sun (M) in degrees
    m = 357.52911 + jc * (35999.05029 - 0.0001537 * jc)

    """
    TRUE SOLAR LONGITUDE
    """
    # Calculate the Eccentricity of Earth's Orbit (e)
    # Calculate the Equation of Center (C) in degrees
    c = math.sin(math.radians(m)) * (1.914602 - jc * (0.004817 + 0.000014 * jc)) + math.sin(math.radians(2 * m)) * (
            0.019993 - 0.000101 * jc) + math.sin(math.radians(3 * m)) * 0.000289
    # Calculate the True Longitude of the Sun (tl) in degrees
    tl = l0 + c

    """
    TRUE SOLAR ANOMALY
    """
    # calculate the true solar anomaly (v)
    v = m + c

    """
    LONGITUDE OF OMEGA
    """
    omega = 125.04 - 1934.136 * jc

    """
    SUN'S RIGHT ASCENSION (DEGREES) (ALPHA)
    """
    # Calculate the Mean Obliquity of the Ecliptic (epsilon) in degrees
    epsilon = 23.439291 - jc * (0.0130042 + 0.00000016 * jc)

    # Calculate the Sun's Right Ascension (alpha) in degrees
    alpha = math.degrees(
        math.atan2(math.cos(math.radians(epsilon)) * math.sin(math.radians(tl)), math.cos(math.radians(tl))))

    # Convert alpha to the range 0-360 degrees
    alpha = (alpha + 360) % 360

    """
    HOUR ANGLE
    """
    lat_rad = math.radians(lat)
    H = math.degrees(math.acos(
        (math.sin(math.radians(-0.83)) - math.sin(math.radians(lat_rad)) * math.sin(
            math.radians(solar_declination))) / (
                math.cos(math.radians(lat_rad)) * math.cos(math.radians(solar_declination)))))

    values = {
        "dec": solar_declination,
        "hour_angle": H,
        "ra": alpha,
        "long_omega": omega,
        "true_solar_anomaly": v,
        "true_solar_longitude": tl,
        "geo_anomaly": m,
        "geo_long": l0,
        "dist": solar_distance,
    }

    return Sun(values)


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def decimalhours(now):
    return (((now.second / 60) + now.minute) / 60) + now.hour


def juliandate(now):
    y = now.year
    m = now.month
    d = now.day
    if m == 1 or m == 2:
        y = y - 1
        m = m + 12
    A = math.floor(y / 100)
    B = 2 - A + math.floor(A / 4)
    C = math.floor(365.25 * y)
    D = math.floor(30.6001 * (m + 1))
    return B + C + D + d + 1720994.5


def gst(jd, dechours):
    S = jd - 2451545
    T = S / 36525
    T0 = 6.697374558 + (2400.051336 * T) + (0.000025862 * T ** 2)
    if T0 < 0:
        T0 = (T0 + abs(T0) // 24 * 24) % 24
    else:
        T0 = T0 % 24
    T0 = T0 + (dechours * 1.002737909)
    if T0 < 0:
        T0 = T0 + 24
    if T0 > 24:
        T0 = T0 - 24
    return T0


def localSiderealTime(long):
    now = datetime.datetime.utcnow()
    jd = juliandate(now)
    dechours = decimalhours(now)
    gstime = gst(jd, dechours)
    LONGITUDE = long
    utcdiff = math.fabs(LONGITUDE) / 15
    if sign(LONGITUDE) == -1:
        lstime = gstime - utcdiff
    else:
        lstime = gstime + utcdiff
    if lstime > 24:
        lstime = lstime - 24
    if lstime < 0:
        lstime = lstime + 24

    raw = lstime
    h = math.floor(lstime)
    m = math.floor((lstime - h) * 60)
    s = math.floor((((lstime - h) * 60) - m) * 60)

    times = {
        "raw": raw,
        "hour": h,
        "minute": m,
        "second": s
    }
    return LST(times)


def declination(l, b):
    e = math.radians(23.4397)  # obliquity of the ecliptic in degrees
    return math.asin(
        math.sin(math.radians(b)) * math.cos(e) + math.cos(math.radians(b)) * math.sin(e) * math.sin(math.radians(l)))


def eclipticLongitude(M):
    rad = math.pi / 180.0
    PI = math.pi

    C = rad * (1.9148 * math.sin(M) + 0.02 * math.sin(2 * M) + 0.0003 * math.sin(3 * M))  # equation of center
    P = rad * 102.9372  # perihelion of the Earth

    return M + C + P + PI


def solarMeanAnomaly(d):
    rad = math.pi / 180.0
    return rad * (357.5291 + 0.98560028 * d)


def daysSinceJ2000():
    # get current date and time in UTC
    now = datetime.datetime.utcnow()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second

    # calculate Julian Date
    a = math.floor((14 - month) / 12)
    Y = year + 4800 - a
    M = month + 12 * a - 3
    D = day
    UT = hour + minute / 60 + second / 3600
    JD = 367 * Y - math.floor(7 * (Y + math.floor((M + 9) / 12)) / 4) + math.floor(
        275 * M / 9) + D + 1721013.5 + UT / 24

    # calculate number of days since J2000.0
    days = (JD - 2451545.0) + (UT - 12) / 24
    return days


def altitude(lat, long):
    d = daysSinceJ2000()
    M = solarMeanAnomaly(d)
    L = eclipticLongitude(M)
    dec = declination(L, 0)
    H = solarHourAngle(long, localSiderealTime(long).raw)
    a = math.asin(math.sin(lat) * math.sin(dec) + math.cos(lat) * math.cos(dec) * math.cos(H))
    return a


def azimuth(lat, long):
    d = daysSinceJ2000()
    M = solarMeanAnomaly(d)
    L = eclipticLongitude(M)
    H = solarHourAngle(long, localSiderealTime(long).raw)
    dec = declination(L, 0)
    return math.atan2(math.sin(H), math.cos(H) * math.sin(lat) - math.tan(dec) * math.cos(lat))


def solarHourAngle(longitude, lst):
    longitude = longitude
    lst = lst
    now = datetime.datetime.now()
    return -15 * ((12 - now) + (now.minute/60) + (now.second/3600))


def rightAscension(l, b):
    e = math.pi/180 * 23.4397
    return math.atan2(math.sin(l) * math.cos(e) - math.tan(b) * math.sin(e), math.cos(l))


def sunRA():
    d = daysSinceJ2000()
    M = solarMeanAnomaly(d)
    L = eclipticLongitude(M)
    return rightAscension(L, 0)


def moonCoords():
    rad = math.pi/180
    d = daysSinceJ2000()
    L = rad * (218.316 + 13.176396 * d)
    M = rad * (134.963 + 13.064993 * d)
    F = rad * (93.272 + 13.229350 * d)
    l = L + rad * 6.289 * math.sin(M)
    b = rad * 5.128 * math.sin(F)
    dt = 385001 - 20905 * math.cos(M)
    values = {
        'ra': rightAscension(l, b),
        'dec': declination(l, b),
        'dist': dt
    }
    return Moon(values)


def astronomicalRefraction(h):
    if h < 0:
        h = 0
    return 0.0002967 / math.tan(h + 0.00312536 / (h + 0.08901179))


def moon_azimuth(h, phi, dec):
    H = h
    return math.atan2(math.sin(H), math.cos(H) * math.sin(phi) - math.tan(dec) * math.cos(phi))


def moon_altitude(H, phi, dec):
    return math.asin(math.sin(phi) * math.sin(dec) + math.cos(phi) * math.cos(dec) * math.cos(H))


def tmpSiderealTime(d, lw):
    return math.radians(280.16 + 360.9856235 * d) - lw


def getMoonPosition(lat, long):
    rad = math.pi / 180
    lw = rad * -long
    phi = rad * lat
    d = daysSinceJ2000()
    c = moonCoords()
    H = tmpSiderealTime(d, lw) - c.ra
    alt = moon_altitude(H, phi, c.dec)
    pa = math.atan2(math.sin(H), math.tan(phi) * math.cos(c.dec) - math.sin(c.dec) * math.cos(H))
    alt += astronomicalRefraction(alt)

    values = {
        'azimuth': moon_azimuth(H, phi, c.dec),
        'altitude': alt,
        'distance': c.dist,
        'parallacticAngle': pa
    }

    return Moon(values)

def planetMeanAnomaly(planet):
    planet = planet.lower()
    m01 = {"mercury":[174.7948, 4.09233445], 
           "venus":[50.4161,1.60213034], 
           "earth":[357.5291,0.98560028], 
           'mars':[19.3730, 0.52402068],
           'jupiter':[20.0202,0.08308529],
           'saturn':[317.0207, 0.03344414],
           'uranus':[141.0498, 0.01172834],
           'neptune':[256.2250, 0.00598103],
           'pluto':[14.882, 0.00396]
          }
    j = juliandate(datetime.datetime.now())
    mlist = m01[planet]
    m0 = mlist[0]
    m1 = mlist[1]
    m = (m0 + m1 * (j-2451545)) % 360
    return m

def zenithAngle(lat):
    a = 90 + lat - getSunData(lat).dec
    zenith_angle = 90 - a
    return zenith_angle


    
