#!/home/vladvv/PycharmProjects/master-checking/myvenv/bin/python
# coding=utf-8


"""
# Документация на masterwiki - http://46.101.237.78/tiki/tiki-index.php?page=MASTERCheckList
1. Из конфиг. файла взять  ccd-master2-url обсерватории
2. подключиться к этому url  по логину и паролю и ответ записать во временный json-file
3. из json-file вытащить значения
ccdw_last_imobj,
ccdw_last_imtime,
ccde_last_imobj,
ccde_last_imtime,
3. полученное значение записать в sqlite3 базу как аттрибут объекта amur_ccdw.last_imobj  и т.д

4. Зависимости, requests, lxml
(myenv) pip install requests, lxml
"""


# To solve exception "Apps aren't loaded yet"
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'masterc.settings'

import django
django.setup()


import configparser
from lxml import html
from lxml import etree
import requests

# To ignore InsecureRequestWarning in stderr
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from mtable.models import MasterSite, Ccd


script_name = 'get_ccd_last_impytpe.py'
script_version = 'v.1.0_20180317'
htusers_cfg_path = '/home/vladvv/master-checking/etc/htusers.cfg'
#htusers_cfg_path = '/home/vladvv/PycharmProjects/master-checking/etc/htusers.cfg'

# Parse httpd_users configuration file
htuconfig = configparser.ConfigParser()
htuconfig.read(htusers_cfg_path)
htusers = htuconfig.sections()
user = htuconfig['user1']['username']
password = htuconfig['user1']['pass']



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


def m2db(url, user, password):
    """
    :return: html content of M2 URL
    """

    try:
        r = requests.get(url, auth=(user, password), verify=False, timeout=10)
        r.raise_for_status()

    except requests.exceptions.ConnectTimeout:
        err_str = 'Oops. Connection timeout occured!'
        # print(err_str)
        return err_str
    except requests.exceptions.ReadTimeout:
        err_str = 'Oops. Read timeout occured'
        # print(err_str)
        return err_str
    except requests.exceptions.ConnectionError:
        err_str = 'Seems like dns lookup failed..'
        # print(err_str)
        return err_str
    except requests.exceptions.HTTPError as err:
        err_str = 'Oops. HTTP Error occured'
        # print(err_str)
        # print('Response is: {content}'.format(content=err.response.content))
        return err_str


    # Тот же massive  но уже просто взятый из текстового файла
    # massive = open("/tmp/1.html", 'r')

    massive = r.content.decode('koi8-r')
    tree = html.fromstring(massive)

    return tree
    #return massive


def get_table_dict(tree):
    """
    Get dict, where key is a image id, and value is dict with image's parameters
    :param tree: Page_tree
    :return table_dict:  dictionary, where
            key is an im_id, for example '227611' and
            value is row_dict, for example
            {'im_id': '227611', 'im_tube': ' EAST ', 'im_date_time': '2018-03-11 17:11:22', 'im_object': 'SURVEY'}
    """
    heads = ['im_id', 'im_date_time', 'im_coord', 'im_exp', 'im_object', 'image_type', 'im_tube', 'im_file_path', 'im_ccd_temp', 'im_filter']
    # Result table_dict, where key is an im_id, and value is row_dict
    table_dict = {}

    values = tree.xpath('.//tr[@class="n"]')

    for bytestring in values:
        # Delete html-tags 'sup' from Coord Column
        f = etree.strip_tags(bytestring, 'sup')
        # Get a 'bytes' object which includes bytestring
        elem = etree.tostring(bytestring)
        # Get a string for parsing
        row_list = etree.XML(elem)
        # list of image attributes
        imattrs = []
        for cell in row_list.iter('td', 'p', 'small'):
            if cell.text is not None:
                # print("%s - %s" % (cell.tag, cell.text))
                imattrs.append(cell.text)
        row_dict = dict(zip(heads, imattrs))
        # Create a table_dict, where key is a im_id, and value is row_dict
        table_dict[row_dict['im_id']] = row_dict

    return table_dict


def get_lastimid(table_dict, sitename, tube='WEST'):
    """
    Get the latest image id
    :param table_dict: dict, where key is a image id, and value is dict with image's parameters
    :param tube: 'WEST' or 'EAST'
    :return last_im_id:  the latest image id
    """
    onetubeimdict = {}
    for key in table_dict.keys():
        # Special case for MASTER-OAFA, where im_tube=''
        if sitename == 'MASTER-OAFA' and tube == 'EAST':
            onetubeimdict[key] = table_dict[key]
        # For all other sites
        else:
            # Del escape characters
            ttube = ''.join(table_dict[key]['im_tube'].split())
            if ttube == tube:
                onetubeimdict[key] = table_dict[key]

    if onetubeimdict:
        id = max(onetubeimdict.keys())
    else:
        id = None

    return id


def get_imattr(table_dict, id, key):
    """
    Get image's attribute
    :param table_dict: dict, where key is a image id, and value is dict with image's parameters
    :param id: Image's ID
    :param key: Image's attribute, for example. 'im_time', 'im_filter', 'im_tube'
    :return last_im_id:  the latest image id
    """
    attr = table_dict[id][key]
    return attr


def get_limattr(url, user, password, sitename, tube, attr):
    """
    Get the lastes image's attribute
    :param url: URL of master2 images
    :param user: login to URL
    :param password: password
    :param tube: 'WEST' or 'EAST'
    :param attr: Image's attribute, for example. 'im_time', 'im_filter', 'im_tube'
    :return imattr:  the latest image id
    """

    #print(name)
    #print(url)
    tree = m2db(url, user, password)
    # print(page)

    try:
        site_table_dict = get_table_dict(tree)
    except:
        site_table_dict = {}

    # print(site_table_dict)

    # Get a last EAST and WEST Image dict (sort by im_id)
    # If there isn't EAST or WEST Image, send alert and imobj-class = table-danger
    lastimid = get_lastimid(site_table_dict, sitename, tube)
    # w_lastimid = get_lastimid(site_table_dict, 'WEST')

    if lastimid:
        imattr = get_imattr(site_table_dict, lastimid, attr)
    else:
        imattr = '-'

    return imattr


def get_limtime_stclass(limtime):
    stclass = 'table-success'
    return stclass

def get_limobj_stclass(limobj):
    stclass = 'table-success'
    return stclass



if __name__ == '__main__':

    sites = MasterSite.objects.all()
    ccds = Ccd.objects.all()

    for s in sites:
        name = s.sitename
        url = s.m2dburl

        #Made dict with two ccd in each site
        for c in ccds:
            if c.sitename == s.sitename and c.tube == 'west':
                west_ccd = c
            elif c.sitename == s.sitename and c.tube == 'east':
                east_ccd = c


        for ccd in (west_ccd, east_ccd):
            # print(ccd.hostname)
            limtime = get_limattr(url, user, password, ccd.sitename, "".join(ccd.tube.upper()), 'im_date_time')
            if limtime != '-':
                limobj = get_limattr(url, user, password, ccd.sitename, "".join(ccd.tube.upper()), 'im_object')
            else:
                limobj = '-'

            # print(limtime)
            # print(limobj)
            limtime_stclass = get_limtime_stclass(limtime)
            limobj_stclass = get_limobj_stclass(limobj)
            # print()


            ccd.last_imobj = limobj
            ccd.last_imobj_stclass = limobj_stclass
            ccd.last_imtime = limtime
            ccd.last_imtime_stclass = limtime_stclass
            ccd.save()

