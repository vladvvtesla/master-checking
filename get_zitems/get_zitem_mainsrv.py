#!/home/vladvv/PycharmProjects/master-checking/myvenv/bin/python
# coding=utf-8


'''
# Документация на masterwiki - http://46.101.237.78/tiki/tiki-index.php?page=MASTERCheckList
1. Составить get  запрос к zabbix-серверу.
2. Этому запросу передать host, например, iac-main-сервер, и item,  например, ping
3. полученное значение item  записать в sqlite3 базу как аттрибут объекта iac-main-сервер.is_ping

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
from mtable.models import MainServer

script_name = 'get_zitem_mainsrv.py'
scipt_version = 'v.1.1_20180309'
cfg_path = "/home/vladvv/master-checking/etc/zbsrv.cfg"
# cfg_path = "/home/vladvv/PycharmProjects/master-checking/etc/zbsrv.cfg"
reason_time = int(900) # (in seconds. Если данные долго не поступали, то status = 'outdated')


item = 'ICMP ping'


def get_zitem(zbsrv, hostid, item):
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

#    print(ZABBIX_SERVER)
#    print(zbsrv_username)
#    print(zbsrv_pass)

    zapi = ZabbixAPI(ZABBIX_SERVER, timeout=5)
    zapi.session.verify=False
    try:
        zapi.login(zbsrv_username, zbsrv_pass)

        items = zapi.item.get(hostids=hostid, output=['itemid', 'name', 'lastvalue', 'lastclock'])
        # print(items)
        if items:
            for item in items:
                # print(item)
                if 'ICMP ping' in item['name']:
                    # print(item['itemid'], item['name'], item['lastvalue'], item['lastclock'])
                    item_lastvalue = int(item['lastvalue'])
                    item_lastts = int(item['lastclock'])
        else:
            # If connection to ZabbixServer exists, but items list is empty
            print ('items list for', hostid, 'is empty')
            item_lastvalue = 504
            item_lastts = int(time.time())
    # If There is no connection to ZabbixServer
    except Exception as e:
        # print('error text', e)
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


def get_host_status(ping_lastvalue, ping_lastclock):
    """
    Calculate and return host_status, based on difference parameters
    :param ping_lastvalue: ping_lastvalue
    :param ping_lastclock:
    :return status: host status
    """

    diff_time = get_diff_time(ping_lastclock)
    # print(diff_time)

    if diff_time < reason_time and ping_lastvalue == 1:
        status = 'OK'
    elif diff_time < reason_time and ping_lastvalue == 0:
        status = 'NO'
    elif diff_time < reason_time and ping_lastvalue == 503:
        status = 'NoConn'
    else:
        status = 'expired'

    return status


def get_host_stclass(status='expired'):
    """
    Mappint status to stsclass, success, warning, danger, etc
    :param status: ON, OFF, maintenace, etc
    :return stsclass: success, warning, danger, etc
    """

    if status == 'OK':
        stclass = "table-success"
    elif status == 'OFF':
        stclass = "table-danger"
    elif status == 'expired':
        stclass = "table-warning"
    elif status == 'NoConn':
        stclass = "table-warning"
    elif status == 'maintenance':
        stclass = "table-info"
    else:
        stclass = 'table-info'

    return stclass



if __name__ == '__main__':

    MainServers = MainServer.objects.all()
    for srv in MainServers:
        # print(srv.hostname)
        # print(srv.zbsrv)
        # print(srv.hostid)

        # If host on maintenance don't execute get_zitem
        if srv.maintenance:
            item_lastvalue, = "0"
            item_lastts = 1519398497
            host_status = "-"
            host_stclass = "table-info"
        else:
            item_lastvalue, item_lastts = get_zitem(srv.zbsrv, srv.hostid, item)
            # print(item_lastts)
            # print(item_lastvalue)

            host_status = get_host_status(item_lastvalue, item_lastts)
            # print(host_status)

            host_stclass = get_host_stclass(host_status)
            # print(host_stclass)
            # print()

        # srv = MainServer.objects.get(hostid=host_id)
        srv.zi_pingval = item_lastvalue
        srv.zi_pingts = item_lastts
        srv.status = host_status
        srv.stclass = host_stclass
        srv.save()

