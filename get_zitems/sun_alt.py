#!/home/vladvv/PycharmProjects/master-checking/myvenv/bin/python
# coding=utf-8


'''
# Документация на masterwiki - http://46.101.237.78/tiki/tiki-index.php?page=MASTERCheckList
1. Из конфиг. файла взять  Latitude и  Longitude  обсерватории
2. На основе этого вычислить высоту Cолнца над горизонтом в обсерватории
3. полученное значение sun_alt записать в sqlite3 базу как аттрибут объекта master-iac.sun_alt

4. Зависимости pyzabbix, requests
(myenv) pip install pyzabbix, requests, pyephem
'''


# To solve exception "Apps aren't loaded yet"
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'masterc.settings'

import django
django.setup()

import ephem
from mtable.models import MasterSite

script_name = 'sun_alt.py'
script_version = 'v.0.1_20180303'

def sun_altitude(lon, lat):
    """
    Import from file a list of already downloaded IDs ,
    IDs is kept in format DDMMYYY.ID
    If file doesn't exists it will be created
    :param lon: Longitude of the site
    :param lat: Latitude of the site
    :return sun_alt:  Altitude of the Sun for the site
    """

    obs = ephem.Observer()
    obs.date = ephem.now()
    obs.lon = lon
    obs.lat = lat
    sun = ephem.Sun(obs)
    sun.compute(obs)

    # Perform -17:06:05.7 to -17
    sun_alt = str(sun.alt).split(":")[0]
    # print(sun_alt)

    return sun_alt


def get_sun_alt_stclass(sun_alt):
    """
    Get sun_alt_status_class for sun_alt
    :param sun_alt: Sun Altitude
    :return stclass:  css-class table-active, table-success etc
    """
    alt = int(sun_alt)
    if alt >= 0:
        stclass = "table-warning"
    elif alt < 0:
        stclass = "table-primary"
    else:
        stclass = "table-info"

    return stclass


if __name__ == '__main__':

    sites = MasterSite.objects.all()
    for s in sites:
        name = s.sitename
        lon = s.lon
        lat = s.lat
        # print (site_name, lat)
        sun_alt = sun_altitude(lon, lat)
        sun_alt_stclass = get_sun_alt_stclass(sun_alt)
        print(s.sitename)
        print(sun_alt)
        print(sun_alt_stclass)
        print()

        s.sun_alt = sun_alt
        s.sun_alt_stclass = sun_alt_stclass
        s.save()

