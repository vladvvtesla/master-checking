from django.db import models
from django.utils import timezone


# Master Host: General attributes of the alll Master Hosts
#class MasterHost(models.Model):
#    sitename = models.CharField(max_length=14)
#    maintenance = models.BooleanField(default=False)
#    zbsrv = models.CharField(max_length=22, default='MASTER-Zabbix-Server-3')
#    hostid = models.IntegerField(default=99999)
#    hostname = models.CharField(max_length=35, default='main-server')
#    ipaddr = models.GenericIPAddressField(default='127.0.0.1')
#    status = models.CharField(max_length=7, default='OK')
#    status = models.CharField(max_length=7, default='OK')
#    stclass = models.CharField(max_length=13, default='table-info')
#
#    def __str__(self):
#        return self.hostname


# MasterSite: MASTER-SAAO, MASTER-IAC etc
class MasterSite(models.Model):
    # author = models.ForeignKey('auth.User')
    created_date = models.DateTimeField(default=timezone.now)
    sitename = models.CharField(max_length=17)
    lat = models.CharField(max_length=12, null=True, blank=True)
    lon = models.CharField(max_length=12, null=True, blank=True)
    elev = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    website = models.URLField(max_length=30, null=True, blank=True)
    m2dburl = models.URLField(max_length=30, null=True, blank=True)
    wfcurl = models.URLField(max_length=30, null=True, blank=True)
    sun_alt = models.SmallIntegerField(default=0, null=True, blank=True)
    sun_alt_stclass = models.CharField(max_length=13, default='table-info')

    def __str__(self):
        return self.sitename

# Main Server: Main Server , Ebox server 
class MainServer(models.Model):
    sitename = models.CharField(max_length=17)
    maintenance = models.BooleanField(default=False)
    zbsrv = models.CharField(max_length=22, default='MASTER-Zabbix-Server-3')
    hostid = models.IntegerField(default=99999)
    hostname = models.CharField(max_length=35, default='main-server')
    ipaddr = models.GenericIPAddressField(default='127.0.0.1')
    zi_pingval = models.SmallIntegerField(default=0)
    zi_pingts = models.IntegerField(default=1519398497)
    status = models.CharField(max_length=7, default='OK')
    stclass = models.CharField(max_length=13, default='table-info')

    def __str__(self):
        return self.hostname

# Head: Amur Head, Tunka Head, etc
class Head(models.Model):
    sitename = models.CharField(max_length=17)
    maintenance = models.BooleanField(default=False)
    zbsrv = models.CharField(max_length=22, default='MASTER-Zabbix-Server-3')
    hostid = models.IntegerField(default=99999)
    hostname = models.CharField(max_length=22, default='amur-head')
    zitem_task_val = models.CharField(max_length=7)
    zitem_task_ts = models.IntegerField(default=1519398497)
    status = models.CharField(max_length=7, default='OK')
    stclass = models.CharField(max_length=13, default='table-info')

    def __str__(self):
        return self.hostname


# Mounts
class Mount(models.Model):
    sitename = models.CharField(max_length=17)
    maintenance = models.BooleanField(default=False)
    zbsrv = models.CharField(max_length=22, default='MASTER-Zabbix-Server-3')
    hostid = models.IntegerField(default=99999)
    hostname = models.CharField(max_length=13, default='amur-mount')
    zi_mstat_val = models.CharField(max_length=7)
    zi_mstat_ts = models.IntegerField(default=1519398497)
    status = models.CharField(max_length=7, default='OK')
    stclass = models.CharField(max_length=13, default='table-info')

    def __str__(self):
        return self.hostname


# Domes
class Dome(models.Model):
    sitename = models.CharField(max_length=17)
    maintenance = models.BooleanField(default=False)
    zbsrv = models.CharField(max_length=22, default='MASTER-Zabbix-Server-3')
    hostid = models.IntegerField(default=99999)
    hostname = models.CharField(max_length=12, default='amur-dome')
    zi_dome_val = models.IntegerField(default=3)
    zi_dome_ts = models.IntegerField(default=1519398497)
    status = models.CharField(max_length=7, default='OK')
    stclass = models.CharField(max_length=13, default='table-info')

    def __str__(self):
        return self.hostname


# CCDs
class Ccd(models.Model):
    sitename = models.CharField(max_length=17)
    exists = models.BooleanField(default=False)
    maintenance = models.BooleanField(default=False)
    zbsrv = models.CharField(max_length=22, default='MASTER-Zabbix-Server-3')
    hostid = models.IntegerField(default=99999)
    ccdid = models.CharField(max_length=3, null=True, blank=True)
    hostname = models.CharField(max_length=19, default='amur-ccd-west')
    tube = models.CharField(max_length=4, default='west')
    last_imobj = models.CharField(max_length=8, default='-')
    last_imobj_stclass = models.CharField(max_length=13, default='table-info')
    last_imtime = models.CharField(max_length=19, default='-')
    last_imtime_stclass = models.CharField(max_length=13, default='table-info')
    zi_mstat_val = models.CharField(max_length=7)
    zi_mstat_ts = models.IntegerField(default=1519398497)
    status = models.CharField(max_length=7, default='OK')
    stclass = models.CharField(max_length=13, default='table-info')

    def __str__(self):
        return self.hostname

# WFCs
class WFC(models.Model):
    sitename = models.CharField(max_length=17)
    exists = models.BooleanField(default=False)
    maintenance = models.BooleanField(default=False)
    zbsrv = models.CharField(max_length=22, default='MASTER-Zabbix-Server-3')
    hostid = models.IntegerField(default=99999)
    wfcid = models.CharField(max_length=6, null=True, blank=True)
    hostname = models.CharField(max_length=22, default='amur-ccd-west')
    ipaddr = models.GenericIPAddressField(default='127.0.0.1')
    tube = models.CharField(max_length=4, default='west')
    last_imobj = models.CharField(max_length=8, default='-')
    last_imobj_stclass = models.CharField(max_length=13, default='table-info')
    last_imtime = models.CharField(max_length=19, default='-')
    last_imtime_stclass = models.CharField(max_length=13, default='table-info')
    zi_mstat_val = models.CharField(max_length=7)
    zi_mstat_ts = models.IntegerField(default=1519398497)
    status = models.CharField(max_length=7, default='OK')
    stclass = models.CharField(max_length=13, default='table-info')

    def __str__(self):
        return self.hostname

# Filters
class Filter(models.Model):
    sitename = models.CharField(max_length=17)
    exists = models.BooleanField(default=False)
    maintenance = models.BooleanField(default=False)
    zbsrv = models.CharField(max_length=22, default='MASTER-Zabbix-Server-3')
    hostid = models.IntegerField(default=99999)
    hostname = models.CharField(max_length=22, default='amur-filter-west')
    tube = models.CharField(max_length=4, default='west')
    zi_filter_val = models.IntegerField(default=9)
    zi_filter_ts = models.IntegerField(default=1519398497)
    display_name = models.CharField(max_length=8, default='W')
    status = models.CharField(max_length=7, default='OK')
    stclass = models.CharField(max_length=13, default='table-info')

    def __str__(self):
        return self.hostname


# Focusers
class Focuser(models.Model):
    sitename = models.CharField(max_length=17)
    exists = models.BooleanField(default=False)
    maintenance = models.BooleanField(default=False)
    zbsrv = models.CharField(max_length=22, default='MASTER-Zabbix-Server-3')
    hostid = models.IntegerField(default=99999)
    hostname = models.CharField(max_length=23, default='amur-ccd-west')
    tube = models.CharField(max_length=4, default='west')
    zi_fpval = models.CharField(max_length=7)
    zi_fpts = models.IntegerField(default=1519398497)
    status = models.CharField(max_length=7, default='OK')
    stclass = models.CharField(max_length=13, default='table-info')

    def __str__(self):
        return self.hostname


# Second Server:
class SecondServer(models.Model):
    sitename = models.CharField(max_length=17)
    exists = models.BooleanField(default=False)
    maintenance = models.BooleanField(default=False)
    zbsrv = models.CharField(max_length=22, default='MASTER-Zabbix-Server-3')
    hostid = models.IntegerField(default=99999)
    hostname = models.CharField(max_length=35, default='main-server')
    ipaddr = models.GenericIPAddressField(default='127.0.0.1')
    zi_pingval = models.SmallIntegerField(default=0)
    zi_pingts = models.IntegerField(default=1519398497)
    status = models.CharField(max_length=7, default='OK')
    stclass = models.CharField(max_length=13, default='table-info')

    def __str__(self):
        return self.hostname



# Ebox server
class Ebox(models.Model):
    sitename = models.CharField(max_length=17)
    exists = models.BooleanField(default=False)
    maintenance = models.BooleanField(default=False)
    zbsrv = models.CharField(max_length=22, default='MASTER-Zabbix-Server-3')
    hostid = models.IntegerField(default=99999)
    hostname = models.CharField(max_length=35, default='main-server')
    ipaddr = models.GenericIPAddressField(default='127.0.0.1')
    zi_pingval = models.SmallIntegerField(default=0)
    zi_pingts = models.IntegerField(default=1519398497)
    status = models.CharField(max_length=7, default='OK')
    stclass = models.CharField(max_length=13, default='table-info')

    def __str__(self):
        return self.hostname


# Actuator
class Actuator(models.Model):
    sitename = models.CharField(max_length=17)
    exists = models.BooleanField(default=True)
    maintenance = models.BooleanField(default=False)
    zbsrv = models.CharField(max_length=22, default='MASTER-Zabbix-Server-3')
    hostid = models.IntegerField(default=99999)
    hostname = models.CharField(max_length=12, default='amur-dome')
    zi_act_val = models.CharField(max_length=9)
    zi_act_ts = models.IntegerField(default=1519398497)
    status = models.CharField(max_length=7, default='OK')
    stclass = models.CharField(max_length=13, default='table-info')

    def __str__(self):
        return self.hostname









