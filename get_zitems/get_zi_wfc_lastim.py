#!/home/vladvv/PycharmProjects/master-checking/myvenv/bin/python
# coding=utf-8


"""
# Документация на masterwiki - http://46.101.237.78/tiki/tiki-index.php?page=MASTERCheckList
1. Составить get  запрос к zabbix-серверу.
2. Этому запросу передать host, например, wfc111339, и item,  например, last_imobj
3. полученное значение item  записать в sqlite3 базу как аттрибут объекта wfc111339.wfcimobj

4. Зависимости pyzabbix, requests
(myenv) pip install pyzabbix, requests
"""


# To solve exception "Apps aren't loaded yet"
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'masterc.settings'

import django
django.setup()

from pyzabbix import ZabbixAPI, ZabbixAPIException
import configparser
import datetime as dt
from datetime import datetime

from mtable.models import MasterSite, WFC


script_name = 'get_zi_wfc_lastim.py'
script_version = 'v.1.2_20190307'
# cfg_path = "/home/vladvv/master-checking/etc/zbsrv.cfg"
cfg_path = "/home/vladvv/PycharmProjects/master-checking/etc/zbsrv.cfg"
reason_time = int(900) # (in seconds. Если данные долго не поступали, то status = 'outdated')

# htusers_cfg_path = '/home/vladvv/master-checking/etc/htusers.cfg'
htusers_cfg_path = '/home/vladvv/PycharmProjects/master-checking/etc/htusers.cfg'

# Parse httpd_users configuration file
htuconfig = configparser.ConfigParser()
htuconfig.read(htusers_cfg_path)
htusers = htuconfig.sections()
user = htuconfig['user1']['username']
password = htuconfig['user1']['pass']

item_regular = 'Time_Stamp'
trigger_regular = 'There are no WFC images last'
# trigger_regular = 'unavailable'


def get_zitem(zbsrv, hostid, item_regular):
    """
    Make a GET.request to ZABBIX.API by pyzabbix ,
    and return a result of request
    :param zbsrv: Zabbix-Server
    :param hostid: For example, iac.main-resver's hostids is 10120
    :param item_regular:  For example, "ccd focus duration"
    :return (item_lastvalue, item_lastclock):
            tuple with results of request (item_lastvalue, item_lastclock)
    """

    # Parse configuration file
    config = configparser.ConfigParser()
    config.read(cfg_path)
    zbsrvs = config.sections()

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
        if items:
            item_lastvalue, item_lastts = None, None
            for item in items:
                if item_regular in item['name']:
                    item_lastvalue = str(item['lastvalue'])
                    item_lastts = int(item['lastclock'])
            # If we didn't found item_lastvalue and item_lastts in items
            if item_lastvalue is None:
                item_lastvalue = 502
            if item_lastts is None:
                item_lastts = (dt.datetime.utcnow() - dt.datetime(1970, 1, 1)).total_seconds()
        else:
            # If connetction to ZabbixServer exists, but items list is empty
            item_lastvalue = 504
            item_lastts = (dt.datetime.utcnow() - dt.datetime(1970, 1, 1)).total_seconds()
    # If There is no connection to ZabbixServer
    except Exception as e:
        # print('error text', e)
        item_lastvalue = 503
        item_lastts = (dt.datetime.utcnow() - dt.datetime(1970, 1, 1)).total_seconds()

    return (item_lastvalue, item_lastts)


def get_ztrigger(zbsrv, hostid, trigger_regular):
    """
    Make a GET.trigger request to ZABBIX.API by pyzabbix ,
    and return a result of request
    :param zbsrv: Zabbix-Server
    :param hostid: For exampe, iac.main-resver's hostids is 10120
    :param item: For example, 'ISMP ping'
    :return (trigger):
            tuple with results of request (item_lastvalue, item_lastclock)
    """

    # Parse configuration file
    config = configparser.ConfigParser()
    config.read(cfg_path)
    zbsrvs = config.sections()

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

        triggers = zapi.trigger.get(hostids=hostid, output=['triggerid', 'description', 'value', 'priority'])
        if triggers:
            trigger_value = None
            for trigger in triggers:
                if trigger_regular in trigger['description']:
                    trigger_value = str(trigger['value'])
            # If we didn't found trigger_regular in triggers
            if trigger_value is None:
                trigger_value = 502
        else:
            # If connetction to ZabbixServer exists, but trigger list is empty
            trigger_value = 504
    # If There is no connection to ZabbixServer
    except Exception as e:
        # print('error text', e)
        trigger_value = 503

    return (trigger_value)


def convert_time(dtime):
    """
    Convert Last Image Time to other format
    :param dtime: - Time in format: 2018-09-20 02:34:06
    :return: convtime - Time in format: 18-09-20 02:34:06
    """

    convtime = '-'
    if dtime == str(0):
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


def get_diff_time(ts):
    """
    Calculate and return difference between current timestamp and other timestump
    :param ts: other timestamp
    :return diff_time: difference in secconds
    """
    ts_utc = dt.datetime.utcfromtimestamp(ts)
    now_utc = dt.datetime.utcnow()
    diff_time = int((now_utc - ts_utc).total_seconds())

    return diff_time


def get_host_val(zvalue, ztimestamp):
    """
    Found out and return Visible Value in Master Equipment Main Page, based on difference parameters
    :param zvalue: value
    :param ztimestamp:
    :return status: visible value
    """

    diff_time = get_diff_time(ztimestamp)

    val_to_stat = {502: 'NoItem',
                   503: 'NoConnz',
                   504: 'expired',
                   0: 'NoConn',
                   '1970-01-01 00:00:00': '-'}
    if diff_time < reason_time:
        if zvalue in val_to_stat.keys():
            value = val_to_stat[zvalue]
        else:
            # Convert Last Image Time to other format
            value = convert_time(zvalue)
    elif diff_time > reason_time:
        value = 'expired'
    else:
        value = 'expired'

    return value


def get_host_stclass(dname='expired', trig_val=0):
    """
    Mapping DisplayName to stsclass: success, warning, danger, etc
    :param dname: 'OK', 'READY', 'SURVEY', '-', , etc
    :param trig_val: trigger value : 1 or 0
    :return stsclass: success, warning, danger, etc
    """

    st_to_stclass = {'expired' : 'table-warning',
                   '-' : 'table-warning'}

    if int(trig_val) == 1:
        stclass = 'table-danger'
    elif int(trig_val) == 502:
        stclass = 'table-warning'
    elif int(trig_val) == 503:
        stclass = 'table-warning'
    elif int(trig_val) == 504:
        stclass = 'table-warning'
    elif int(trig_val) == 0:
        if dname in st_to_stclass:
            stclass =  st_to_stclass[dname]
        else:
            stclass = 'table-success'
    else:
        stclass = 'table-warning'

    return stclass


if __name__ == '__main__':

    sites = MasterSite.objects.all()
    wfcs = WFC.objects.all()

    for s in sites:
        name = s.sitename
        url = s.wfcurl

        # Made dict with two wfc in each site
        for wfc in wfcs:
            if wfc.sitename == s.sitename and wfc.tube == 'west':
                west_wfc = wfc
            elif wfc.sitename == s.sitename and wfc.tube == 'east':
                east_wfc = wfc

        for wfc in (west_wfc, east_wfc):
            if wfc.exists:
                # print('')
                # print(wfc.hostname)
                # print(wfc.wfcid)
                item_lastvalue, item_lastts = get_zitem(wfc.zbsrv, wfc.hostid, item_regular)
                trigger_value = get_ztrigger(wfc.zbsrv, wfc.hostid, trigger_regular)

                host_val = get_host_val(item_lastvalue, item_lastts)
                host_val_stclass = get_host_stclass(host_val, trigger_value)

            else:
                host_val = '-'
                host_val_stclass = 'table-info'

            wfc.last_imtime = host_val
            wfc.last_imtime_stclass = host_val_stclass
            wfc.save()