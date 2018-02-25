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
import time, configparser, ephem
import datetime as dt
from mtable.models import MainServer

script_name = 'get_zitem.py'
scipt_version = 'v.0.0.2_20180221'
cfg_path = 'etc/zbsrv.cfg'
reason_time = int(900) # (in seconds. Если данные долго не поступали, то status = 'outdated')

zbsrv = 'MASTER-Zabbix-Server-3'
host_id = 10105
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
    else:
        srv = zbsrvs[1]

    #print(zbsrv2)
    #print(zbsrv3)

    ZABBIX_SERVER = 'http://' + config[srv]['zbsrv_ip'] + '/zabbix'
    zbsrv_username = config[srv]['zbsrv_username']
    zbsrv_pass = config[srv]['zbsrv_pass']

    #print(ZABBIX_SERVER)
    #print(zbsrv_username)
    #print(zbsrv_pass)

    zapi = ZabbixAPI(ZABBIX_SERVER)
    zapi.session.verify=False
    zapi.login(zbsrv_username, zbsrv_pass)

    items = zapi.item.get(hostids=hostid, output=['itemid', 'name', 'lastvalue', 'lastclock'])
    # print(items)
    for item in items:
        # print(item)
        if 'ICMP ping' in item['name']:
            # print(item['itemid'], item['name'], item['lastvalue'], item['lastclock'])
            item_id = item['itemid']
            item_name = item['name']
            item_lastvalue = int(item['lastvalue'])
            item_lastclock = int(item['lastclock'])

    return (item_lastvalue, item_lastclock)


def get_diff_time(ts):
    """
    Calculate and return difference between current timestamp and other timestump
    :param ts: other timestamp
    :return diff_time: difference in secconds
    """

    ts_utc = dt.datetime.utcfromtimestamp(ts)
    print(ts_utc)

    now_utc = dt.datetime.utcnow()
    print(now_utc)

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
    print(diff_time)

    if diff_time < reason_time and ping_lastvalue == 1:
        status = 'OK'
    elif diff_time < reason_time and ping_lastvalue == 0:
        status = 'NO'
    else:
        status = 'outdated'

    return status



if __name__ == '__main__':

    item_lastvalue, item_lastts = get_zitem(zbsrv, host_id, item)
    print(item_lastts)
    print(item_lastvalue)

    host_status = get_host_status(item_lastvalue, item_lastts)
    print(host_status)

    # Write ping_lastvalue, ping_lastclock, to db.SQLite3
    s = MainServer.objects.get(hostid=host_id)
    s.zitem_ping_val = item_lastvalue
    s.zitem_ping_ts = item_lastts
    s.status = host_status
    s.save()