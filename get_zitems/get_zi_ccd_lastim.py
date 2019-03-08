#!/home/vladvv/PycharmProjects/master-checking/myvenv/bin/python
# coding=utf-8


"""
# Документация на masterwiki - http://46.101.237.78/tiki/tiki-index.php?page=MASTERCheckList
1. Составить get  запрос к zabbix-серверу.
2. Этому запросу передать host, например, SAAO CCD WEST, и item,  например, last_imobj
3. полученное значение item  записать в sqlite3 базу как аттрибут объекта SAAO_CCD_WEST.wfcimobj

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

from mtable.models import MasterSite, Ccd


script_name = 'get_zi_ccd_lastim.py'
script_version = 'v.1.0_20190307'
# cfg_path = "/home/vladvv/master-checking/etc/zbsrv.cfg"
cfg_path = "/home/vladvv/PycharmProjects/master-checking/etc/zbsrv.cfg"
reason_time = int(900) # (in seconds. Если данные долго не поступали, то status = 'outdated')

# htusers_cfg_path = '/home/vladvv/master-checking/etc/htusers.cfg'
htusers_cfg_path = '/home/vladvv/PycharmProjects/master-checking/etc/htusers.cfg'

limtime_regular = 'Time_Stamp'
limobj_regular = 'Object'
trigreg_noccdim = 'There are no CCD images last'
trigreg_focustoolong = 'focus too long'


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
        # print('items:', items)
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
        item_lastvalue = 503
        item_lastts = (dt.datetime.utcnow() - dt.datetime(1970, 1, 1)).total_seconds()

    return (item_lastvalue, item_lastts)


def get_ztrigger(zbsrv, hostid, trigger_regular):
    """
    Make a GET.trigger request to ZABBIX.API by pyzabbix ,
    and return a result of request
    :param zbsrv: Zabbix-Server
    :param hostid: For example, iac.main-resver's hostids is 10120
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
        # print(triggers)
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


def get_limobj_val(zvalue, ztimestamp):
    """
    Found out and return Visible Value in Master Equipment Main Page, based on difference parameters
    :param zvalue: value
    :param ztimestamp:
    :return status: visible value
    """

    diff_time = get_diff_time(ztimestamp)
    # print(diff_time)

    val_to_stat = {502: 'NoItem',
                   503: 'NoConnz',
                   504: 'expired',
                   0: 'NoConn'}
    if diff_time < reason_time:
        if zvalue in val_to_stat.keys():
            value = val_to_stat[zvalue]
        else:
            # Convert Last Image Time to other format
            value = zvalue
    elif diff_time > reason_time:
        value = 'expired'
    else:
        value = 'expired'

    return value


def get_host_stclass(st='expired', trig_ccd=0, trig_focus=0):
    """
    Mapping DisplayName to stsclass: success, warning, danger, etc
    :param st: 'OK', 'READY', 'SURVEY', '-', , etc
    :param trig_ccd: trigger value : 1 or 0
    :param trig_focus: trigger value : 1 or 0
    :return stsclass: success, warning, danger, etc
    Check correctness
    >>> get_host_stclass('expired', 1, 0)
    'table-danger'
    >>> get_host_stclass('expired', 1, 1)
    'table-danger'
    >>> get_host_stclass('expired', 0, 1)
    'table-danger'
    >>> get_host_stclass('expired', 0, 0)
    'table-warning'
    >>> get_host_stclass('190307 10:36:32', 0, 0)
    'table-success'
    """

    st_to_stclass = {502 : 'table-warning',
                     503: 'table-warning',
                     504: 'table-warning',
                     'expired' : 'table-warning',
                     '-' : 'table-warning'}

    trig_max = int(max(trig_ccd, trig_focus))

    if trig_max in st_to_stclass.keys():   #  No Data
        stclass = st_to_stclass[st]
    elif trig_max == 1:                    #  One of the trggers in PROBLEM status
        stclass = 'table-danger'
    elif st in st_to_stclass.keys():       #  There aren't  Triggers, but Item Value is in special list
        stclass = st_to_stclass[st]
    elif trig_max == 0:                    #  That is OK
        stclass = 'table-success'
    else:
        stclass = 'table-warning'          #  All other cases

    return stclass


if __name__ == '__main__':

    import doctest
    doctest.testmod()

    sites = MasterSite.objects.all()
    ccds = Ccd.objects.all()

    for s in sites:
        name = s.sitename
        # url = s.ccdurl

        # Made dict with two ccd in each site
        for ccd in ccds:
            if ccd.sitename == s.sitename and ccd.tube == 'west':
                west_ccd = ccd
            elif ccd.sitename == s.sitename and ccd.tube == 'east':
                east_ccd = ccd

        for ccd in (west_ccd, east_ccd):
            if ccd.exists:
                limtime_lastvalue, limtime_lastts = get_zitem(ccd.zbsrv, ccd.hostid, limtime_regular)
                limobj_lastvalue, limobj_lastts = get_zitem(ccd.zbsrv, ccd.hostid, limobj_regular)
                trig_noccdim = get_ztrigger(ccd.zbsrv, ccd.hostid, trigreg_noccdim)
                trig_focustoolong = get_ztrigger(ccd.zbsrv, ccd.hostid, trigreg_focustoolong)

                limtime = get_host_val(limtime_lastvalue, limtime_lastts)
                limobj = get_limobj_val(limobj_lastvalue, limobj_lastts)

                limtime_stclass = get_host_stclass(limtime, trig_noccdim, trig_focustoolong)
                limobj_stclass = limtime_stclass

            else:
                limobj = '-'
                limobj_stclass = 'table-info'
                limtime = '-'
                limtime_stclass = 'table-info'

            ccd.last_imobj = limobj
            ccd.last_imobj_stclass = limobj_stclass
            ccd.last_imtime = limtime
            ccd.last_imtime_stclass = limtime_stclass
            ccd.save()