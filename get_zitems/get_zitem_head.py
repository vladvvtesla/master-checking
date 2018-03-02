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
from mtable.models import Head

script_name = 'get_zitem_head.py'
scipt_version = 'v.0.1_20180302'
cfg_path = "../etc/zbsrv.cfg"
reason_time = int(900) # (in seconds. Если данные долго не поступали, то status = 'outdated')

zbsrv = 'MASTER-Zabbix-Server-3'
host_id = 10105
item_regular = 'head_status'


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
    else:
        srv = zbsrvs[1]



    ZABBIX_SERVER = 'http://' + config[srv]['zbsrv_ip'] + '/zabbix'
    zbsrv_username = config[srv]['zbsrv_username']
    zbsrv_pass = config[srv]['zbsrv_pass']

    # print(ZABBIX_SERVER)
    # print(zbsrv_username)
    # print(zbsrv_pass)

    zapi = ZabbixAPI(ZABBIX_SERVER)
    zapi.session.verify=False
    zapi.login(zbsrv_username, zbsrv_pass)

    items = zapi.item.get(hostids=hostid, output=['itemid', 'name', 'lastvalue', 'lastclock'])
    # print(items)
    for item in items:
        # print(item)
        if item_regular in item['name']:
            # print(item['itemid'], item['name'], item['lastvalue'], item['lastclock'])
            item_id = item['itemid']
            item_name = item['name']
            item_lastvalue = int(item['lastvalue'])
            item_lastts = int(item['lastclock'])
        # else:
        #    item_lastvalue = 0
        #    item_lastts = 0

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


def get_host_status(lastvalue, lastclock):
    """
    Calculate and return host_status, based on difference parameters
    :param lastvalue: lastvalue
    :param lastclock: lastclock
    :return status: host status
    """

    diff_time = get_diff_time(lastclock)
    print(diff_time)

    val_to_stat = {0 : "NoConnection",
                   1 : "Unknown",
                   2 : "Parked",
                   3 : "Free",
                   4 : "FOCUS",
                   5 : "BIAS",
                   6 : "DARK",
                   7 : "FLAT",
                   8 : "Moon",
                   9 : "Survey",
                   10 : "Inspect",
                   11 : "Alert"}

    if diff_time < reason_time:
        status =  val_to_stat[lastvalue]
    elif diff_time > reason_time:
        status = 'expired'
    else:
        status = 'expired'

    return status


def get_host_statusclass(status='expired'):
    """
    Mappint status to statusclass, success, warning, danger, etc
    :param status: ON, OFF, maintenace, etc
    :return statusclass: success, warning, danger, etc
    """

    if status == 'expired':
        statusclass = "table-warning"
    elif status == 'unknown':
        statusclass = "table-warning"
    elif status == 'maintenance':
        statusclass = "table-info"
    else:
        statusclass = 'table-success'

    return statusclass



if __name__ == '__main__':

    Heads = Head.objects.all()
    for host in Heads:
        print(host.hostname)
        # print(host.zbsrv)
        # print(host.hostid)

        item_lastvalue, item_lastts = get_zitem(host.zbsrv, host.hostid, item_regular)
        # print(item_lastts)
        print(item_lastvalue)

        host_status = get_host_status(item_lastvalue, item_lastts)
        print(host_status)

        host_statusclass = get_host_statusclass(host_status)
        print(host_statusclass)
        print()

        # srv = MainServer.objects.get(hostid=host_id)
        host.zitem_task_val = item_lastvalue
        host.zitem_task_ts = item_lastts
        host.status = host_status
        host.statusclass = host_statusclass
        host.save()

