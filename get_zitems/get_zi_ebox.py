#!/home/vladvv/PycharmProjects/master-checking/myvenv/bin/python
# coding=utf-8


'''
#
Documentation onasterwiki - http://46.101.237.78/tiki/tiki-index.php?page=MASTERCheckList
1. Make a GET-request to zabbix-server.
2. including host-name and item, for example, iac-mount and mount_status
3. Obtained item  put into sqlite3 database as a iac-mount.mountst

4. Dependencies pyzabbix, requests
(myenv) pip install pyzabbix, requests
'''


# To solve exception "Apps aren't loaded yet"
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'masterc.settings'

import django
django.setup()

from pyzabbix import ZabbixAPI, ZabbixAPIException
import configparser
import datetime as dt
import time
from mtable.models import Ebox

script_name = 'get_zi_ebox.py'
scipt_version = 'v.1.0_20190830'
cfg_path = "/home/vladvv/master-checking/etc/zbsrv.cfg"
# cfg_path = "/home/vladvv/PycharmProjects/master-checking/etc/zbsrv.cfg"
reason_time = int(900) # (in seconds. Если данные долго не поступали, то status = 'expired')

item_regular = 'ICMP ping'


def get_zitem(zbsrv, hostid, item_regular):
    """
    Make a GET.request to ZABBIX.API by pyzabbix ,
    and return a result of request
    :param zbsrv: Zabbix-Server
    :param hostid: For exampe, iac.main-resver's hostids is 10120
    :param item: For example, 'ISMP ping'
    :return (item_lastvalue, item_lastclock):
            tuple with results of request (item_lastvalue, item_lastclock)
    """

    # Parse configuration file
    config = configparser.ConfigParser()
    config.read(cfg_path)
    zbsrvs = config.sections()
    # print(zbsrvs)

    if zbsrv in zbsrvs[0]:
        srv = zbsrvs[0]
    elif zbsrv in zbsrvs[1]:
        srv = zbsrvs[1]
    else:
        srv = zbsrvs[2]

    ZABBIX_SERVER = 'http://' + config[srv]['zbsrv_ip'] + '/zabbix'
    zbsrv_username = config[srv]['zbsrv_username']
    zbsrv_pass = config[srv]['zbsrv_pass']

    # print(ZABBIX_SERVER)
    # print(zbsrv_username)
    # print(zbsrv_pass)

    zapi = ZabbixAPI(ZABBIX_SERVER, timeout=5)
    zapi.session.verify=False
    try:
        zapi.login(zbsrv_username, zbsrv_pass)

        items = zapi.item.get(hostids=hostid, output=['itemid', 'name', 'lastvalue', 'lastclock'])
        # print(items)
        if items:
            for item in items:
                # print(item)
                if item_regular in item['name']:
                    # print(item['itemid'], item['name'], item['lastvalue'], item['lastclock'])
                    item_lastvalue = int(item['lastvalue'])
                    item_lastts = int(item['lastclock'])
                    break
                else:
                    # print('There is no ', item_regular, ' in items list')
                    item_lastvalue = 505
                    item_lastts = int(time.time())
        else:
            # If connetction to ZabbixServer exists, but items list is empty
            # print('items list for', hostid, 'is empty')
            item_lastvalue = 504
            item_lastts = int(time.time())
    # If There is no connection to ZabbixServer
    except Exception as e:
        # print('error text - ', e)
        item_lastvalue = 503
        item_lastts = int(time.time())

    return (item_lastvalue, item_lastts)


def get_diff_time(ts):
    """
    Calculate and return difference between current timestamp and other timestump
    :param ts: other timestamp
    :return diff_time: difference in secconds
    """

    ts_utc = dt.datetime.utcfromtimestamp(ts)
    # print(ts_utc)

    now_utc = dt.datetime.utcnow()
    # print(now_utc)

    diff_time = int((now_utc - ts_utc).total_seconds())
    # print(diff_time)

    return diff_time


def get_display_name(lastvalue, lastclock, hdefault_dname):
    """
    Calculate and return host_status, based on difference parameters
    :param lastvalue: lastvalue
    :param lastclock: lastclock
    :param hdefault_dname:  host default display name
    :return status: host status
    """

    diff_time = get_diff_time(lastclock)
    # print(diff_time)

    val_to_stat = {505 : 'NoItem',
                   503 : 'NoConnz',
                   504: 'ex',
                   0 : 'Down',
                   1 : hdefault_dname,
                   }

    if diff_time < reason_time:
        dname =  val_to_stat[lastvalue]
    elif diff_time > reason_time:
        dname = 'ex'
    else:
        dname = 'ex'

    return dname



def get_host_status(dname, lastclock, hdefault_dname):
    """
    Calculate and return host_status, based on difference parameters
    :param lastvalue: lastvalue
    :param lastclock: lastclock
    :param hdefault_dname: host default display name
    :return status: host status
    """

    diff_time = get_diff_time(lastclock)
    # print(diff_time)

    val_to_stat = {'NoItem' : 'expired',
                   'NoConnz' : 'danger',
                   'ex' : 'expired',
                   'Down' : 'Down',
                   hdefault_dname : 'UP',
                   }

    if diff_time < reason_time:
        status =  val_to_stat[dname]
    elif diff_time > reason_time:
        status = 'expired'
    else:
        status = 'expired'

    return status


def get_host_stclass(status='expired',):
    """
    Mappint status to stsclass, success, warning, danger, etc
    :param status: ON, OFF, maintenace, etc
    :param hdefault_dname: host default display name
    :return stsclass: success, warning, danger, etc
    """

    st_to_stclass = {'danger' : 'table-danger',
                     'expired' : 'table-warning',
                     'Down': 'table-danger',
                     'UP' : 'table-success'}

    if status in st_to_stclass:
        stclass =  st_to_stclass[status]
    else:
        stclass = 'table-info'

    return stclass



if __name__ == '__main__':

    hosts = Ebox.objects.all()
    for host in hosts:
        # print()
        # print(host.hostname)
        # print(host.zbsrv)
        # print(host.hostid)

        # If host on maintenance don't execute get_zitem
        if host.maintenance:
            item_lastvalue = "0"
            item_lastts = 1519398497
            display_name = "-"
            host_status = "-"
            host_stclass = "table-info"
            # If host not exists don't execute get_zitem
        elif not host.exists:
            item_lastvalue = "0"
            item_lastts = 1519398497
            display_name = "-"
            host_status = "-"
            host_stclass = "table-info"
        else:
            item_lastvalue, item_lastts = get_zitem(host.zbsrv, host.hostid, item_regular)
            # print("item_lastvalue: ", item_lastvalue)
            # print("item_lastts: ", item_lastts)

            display_name = get_display_name(item_lastvalue, item_lastts, host.default_dname)
            # print("display_name: ", display_name)

            host_status = get_host_status(display_name, item_lastts, host.default_dname)
            # print("host_status: ", host_status)

            host_stclass = get_host_stclass(host_status)
            # print("host_stclass: ", host_stclass)
            # print()

        host.zi_pingval = item_lastvalue
        host.zi_pingts = item_lastts
        host.display_name = display_name
        host.status = host_status
        host.stclass = host_stclass
        host.save()
