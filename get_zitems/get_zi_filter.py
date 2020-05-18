#!/home/vladvv/PycharmProjects/master-checking/myvenv/bin/python
# coding=utf-8


'''
# Документация на masterwiki - http://46.101.237.78/tiki/tiki-index.php?page=MASTERCheckList
1. Составить get  запрос к zabbix-серверу.
2. Этому запросу передать host, например, iac-mount, и item,  например, mount_status
3. полученное значение item  записать в sqlite3 базу как аттрибут объекта iac-mount.mountst

4. Зависимости pyzabbix, requests
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
from mtable.models import Filter

script_name = 'get_zi_filter.py'
scipt_version = 'v.1.1_20181006'
cfg_path = "/home/vladvv/master-checking/etc/zbsrv.cfg"
# cfg_path = "/home/vladvv/PycharmProjects/master-checking/etc/zbsrv.cfg"
reason_time = int(900) # (in seconds. Если данные долго не поступали, то status = 'outdated')

item_regular = 'filter'


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
    else:
        srv = zbsrvs[1]



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
                else:
                    print('There is no ', item_regular, ' in items list')
                    item_lastvalue = 505
                    item_lastts = int(time.time())
        else:
            # If connetction to ZabbixServer exists, but items list is empty
            print('items list for', hostid, 'is empty')
            item_lastvalue = 504
            item_lastts = int(time.time())
    # If There is no connection to ZabbixServer
    except Exception as e:
        print('error text - ', e)
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


def get_display_name(lastvalue, lastclock):
    """
    Calculate and return host_status, based on difference parameters
    :param lastvalue: lastvalue
    :param lastclock: lastclock
    :return status: host status
    """

    diff_time = get_diff_time(lastclock)
    # print(diff_time)

    val_to_stat = {503 : 'NoConnz',
                   504: 'expired',
                   0 : 'NoConn',
                   1 : 'ERR',
                   2 : 'BLANK',
                   3 : 'CHANGING',
                   4: 'FAULT',
                   5: 'B',
                   6: 'V',
                   7: 'R',
                   8: 'I',
                   9: 'W',
                   10: 'C',
                   11: 'P',
                   12: 'Q'}

    if diff_time < reason_time:
        dname =  val_to_stat[lastvalue]
    elif diff_time > reason_time:
        dname = 'expired'
    else:
        dname = 'expired'

    return dname



def get_host_status(dname, lastclock):
    """
    Calculate and return host_status, based on difference parameters
    :param lastvalue: lastvalue
    :param lastclock: lastclock
    :return status: host status
    """

    diff_time = get_diff_time(lastclock)
    # print(diff_time)

    val_to_stat = {'NoConnz' : 'danger',
                   'expired' : 'expired',
                   'NoConn' : 'expired',
                   'ERR' : 'expired',
                   'BLANK' : 'OK',
                   'CHANGING' : 'danger',
                   'FAULT' : 'danger',
                   'B' : 'OK',
                   'V' : 'OK',
                   'R' : 'OK',
                   'I' : 'OK',
                   'W' : 'OK',
                   'C' : 'OK',
                   'P' : 'OK',
                   'Q' : 'OK',}

    if diff_time < reason_time:
        status =  val_to_stat[dname]
    elif diff_time > reason_time:
        status = 'expired'
    else:
        status = 'expired'

    return status


def get_host_stclass(status='expired'):
    """
    Mappint status to stsclass, success, warning, danger, etc
    :param status: ON, OFF, maintenace, etc
    :return stsclass: success, warning, danger, etc
    """

    st_to_stclass = {'danger' : 'table-danger',
                   'expired' : 'table-warning',
                   'OK' : 'table-success'}

    if status in st_to_stclass:
        stclass =  st_to_stclass[status]
    else:
        stclass = 'table-info'

    return stclass



if __name__ == '__main__':

    hosts = Filter.objects.all()
    for host in hosts:
        # print()
        # print(host.hostname)
        # print(host.zbsrv)
        # print(host.hostid)

        # If host on maintenance don't execute get_zitem
        if host.maintenance:
            item_lastvalue = "9"
            item_lastts = 1519398497
            display_name = "-"
            host_status = "-"
            host_stclass = "table-info"
            # If host not exists don't execute get_zitem
            # Exclude for MASTR-SAAO
        elif host.hostname == 'oafa-filter-east':
            item_lastvalue = "2"
            item_lastts = 1519398497
            display_name = "BLANK"
            host_status = "OK"
            host_stclass = "table-success"
        elif not host.exists:
            item_lastvalue = "9"
            item_lastts = 1519398497
            display_name = "-"
            host_status = "-"
            host_stclass = "table-info"
        else:
            item_lastvalue, item_lastts = get_zitem(host.zbsrv, host.hostid, item_regular)
            # print("item_lastvalue: ", item_lastvalue)
            # print("item_lastts: ", item_lastts)

            display_name = get_display_name(item_lastvalue, item_lastts)
            # print("display_name: ", display_name)

            host_status = get_host_status(display_name, item_lastts)
            # print("host_status: ", host_status)

            host_stclass = get_host_stclass(host_status)
            # print("host_stclass: ", host_stclass)
            # print()

        # host.zi_dome_val - digit code from zabbix-server
        # host.status = what is showed on main-table
        host.zi_filter_val = item_lastvalue
        host.zi_filter_ts = item_lastts
        host.display_name = display_name
        host.status = host_status
        host.stclass = host_stclass
        host.save()

