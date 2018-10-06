#!/home/vladvv/PycharmProjects/master-checking/myvenv/bin/python
# coding=utf-8


"""
# Документация на masterwiki - http://46.101.237.78/tiki/tiki-index.php?page=MASTERCheckList
1. Из конфиг. файла взять  wfc-url обсерватории
2. подключиться к этому url  по логину и паролю и ответ записать во временный json-file
3. из json-file вытащить значения
wfc111339_last_imobj,
wfc111339_last_imtime,
wfc111340_last_imobj,
wfc111340_last_imtime,
3. полученное значение записать в sqlite3 базу как аттрибут объекта tunka_wfc111339.last_imobj  и т.д

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
from datetime import datetime, date, time

# To ignore InsecureRequestWarning in stderr
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from mtable.models import MasterSite, WFC


script_name = 'get_wfc_last_imtype.py'
script_version = 'v.1.1_20180920'
#htusers_cfg_path = '/home/vladvv/master-checking/etc/htusers.cfg'
htusers_cfg_path = '/home/vladvv/PycharmProjects/master-checking/etc/htusers.cfg'

# Parse httpd_users configuration file
htuconfig = configparser.ConfigParser()
htuconfig.read(htusers_cfg_path)
htusers = htuconfig.sections()
user = htuconfig['user1']['username']
password = htuconfig['user1']['pass']



def wfcpage_tree(url, user, password):
    """
    :return: html content of wfc URL as tree
    """

    try:
        r = requests.get(url, auth=(user, password), verify=False, timeout=60)
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


def get_lastimid(table_dict, sitename, wfcid='100628'):
    """
    Get the latest image id
    :param table_dict: dict, where key is a image id, and value is dict with image's parameters
    :param tube: '100628' , '100628', etc
    :return last_im_id:  the latest image id
    """
    onewfcimdict = {}
    for key in table_dict.keys():
#        # Special case for MASTER-OAFA, where im_tube=''
#        if sitename == 'MASTER-OAFA' and tube == 'EAST':
#            onetubeimdict[key] = table_dict[key]
#        # For all other sites
#        else:
        # Del escape characters
        twfc = ''.join(table_dict[key]['im_tube'].split())
        if int(twfc) == int(wfcid):
            onewfcimdict[key] = table_dict[key]

    if onewfcimdict:
        id = max(onewfcimdict.keys())
    else:
        id = 10001

    return int(id)


def get_imattr(table_dict, id, key):
    """
    Get image's attribute
    :param table_dict: dict, where key is a image id, and value is dict with image's parameters
    :param id: Image's ID
    :param key: Image's attribute, for example. 'im_time', 'im_filter', 'im_tube'
    :return last_im_id:  the latest image id
    """
    value = table_dict[str(id)][key]
    return value


def get_limattr(url, user, password, sitename, wfcid, attr):
    """
    Get the lastes image's attribute
    :param url: URL of master wfc images
    :param user: login to URL
    :param password: password
    :param wfcid: '100628' , '100629', etc
    :param attr: Image's attribute, for example. 'im_time', 'im_filter', 'im_tube'
    :return imattr:  the latest image id
    """

    #print(name)
    #print(url)
    tree = wfcpage_tree(url, user, password)
    # print(tree)

    try:
        site_table_dict = get_table_dict(tree)
    except:
        site_table_dict = {}

    # print(site_table_dict)

    # Get a last 100628 and 100629 Image dict (sort by im_id)
    # If there isn't 100628 or 100629 Image, send alert and imobj-class = table-danger
    lastimid = get_lastimid(site_table_dict, sitename, wfcid)
    # print(lastimid)

    # it lastimid == '-', there is no image from wfcid in the wfcurl. It's error
    if lastimid == 10001:
        imattr = '-'
    else:
        imattr = get_imattr(site_table_dict, lastimid, attr)

    return imattr


def convert_time(dtime):
    """
    Convert Last Image Time to other format
    :param limtime - Time in format: 2018-09-20 02:34:06
    :return: convtime - Time in format: 18-09-20 02:34:06
    """

    if dtime == '-':
        convtime = '-'
    else:
        try:
            dt = datetime.strptime(dtime, "%Y-%m-%d %H:%M:%S.%f")
            convtime = dt.strftime("%y%m%d %H:%M:%S")
        except ValueError:
            dt = datetime.strptime(dtime, "%Y-%m-%d %H:%M:%S")
            convtime = dt.strftime("%y%m%d %H:%M:%S")
        except TypeError:
            print(dtime)

    return convtime


def get_limtime_stclass(limtime):
    stclass = 'table-success'
    return stclass


def get_limobj_stclass(limobj):
    stclass = 'table-success'
    return stclass



if __name__ == '__main__':

    sites = MasterSite.objects.all()
    wfcs = WFC.objects.all()

    for s in sites:
        name = s.sitename
        url = s.wfcurl

        #Made dict with two wfc in each site
        for wfc in wfcs:
            if wfc.sitename == s.sitename and wfc.tube == 'west':
                west_wfc = wfc
            elif wfc.sitename == s.sitename and wfc.tube == 'east':
                east_wfc = wfc

        for wfc in (west_wfc, east_wfc):
            if wfc.exists:
                #print('')
                #print(wfc.hostname)
                #print(wfc.wfcid)
                limtime_raw = get_limattr(url, user, password, wfc.sitename, wfc.wfcid, 'im_date_time')
                if limtime_raw != '-':
                    limobj = get_limattr(url, user, password, wfc.sitename, wfc.wfcid, 'im_object')
                else:
                    limobj = '-'

                # Convert Last Image Time to other format
                limtime = convert_time(limtime_raw)
                # print(limtime)

                #print(limtime)
                #print(limobj)
                limtime_stclass = get_limtime_stclass(limtime)
                limobj_stclass = get_limobj_stclass(limobj)
                # print()
            else:
                limobj = '-'
                limobj_stclass = 'table-info'
                limtime = '-'
                limtime_stclass = 'table-info'


            wfc.last_imtime = limtime
            wfc.last_imtime_stclass = limtime_stclass
            wfc.last_imobj = limobj
            wfc.last_imobj_stclass = limobj_stclass
            wfc.save()

