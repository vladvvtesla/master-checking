from django.db import models
from django.utils import timezone


# MasterSite: MASTER-SAAO, MASTER-IAC etc
class MasterSite(models.Model):
    # author = models.ForeignKey('auth.User')
    created_date = models.DateTimeField(default=timezone.now)
    sitename = models.CharField(max_length=14)
    lat = models.CharField(max_length=12, null=True, blank=True)
    lon = models.CharField(max_length=12, null=True, blank=True)
    elev = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    website = models.URLField(max_length=30, null=True, blank=True)
    sun_alt = models.SmallIntegerField(default=0, null=True, blank=True)
    sun_alt_stclass = models.CharField(max_length=13, default='table-info')

    def __str__(self):
        return self.sitename

# Main Server: Main Server , Ebox server 
class MainServer(models.Model):
    sitename = models.CharField(max_length=14)
    maintenance = models.BooleanField(default=False)
    zbsrv = models.CharField(max_length=22, default='MASTER-Zabbix-Server-3')
    hostid = models.IntegerField(default=99999)
    hostname = models.CharField(max_length=35, default='main-server')
    ipaddr = models.GenericIPAddressField(default='127.0.0.1')
    zitem_ping_val = models.SmallIntegerField(default=0)
    zitem_ping_ts = models.IntegerField(default=1519398497)
    status = models.CharField(max_length=7, default='OK')
    statusclass = models.CharField(max_length=13, default='table-info')


    def __str__(self):
        return self.hostname

# Head: Amur Head, Tunka Head, etc
class Head(models.Model):
    sitename = models.CharField(max_length=14)
    maintenance = models.BooleanField(default=False)
    zbsrv = models.CharField(max_length=22, default='MASTER-Zabbix-Server-3')
    hostid = models.IntegerField(default=99999)
    hostname = models.CharField(max_length=12, default='main-server')
    zitem_task_val = models.CharField(max_length=7)
    zitem_task_ts = models.IntegerField(default=1519398497)
    status = models.CharField(max_length=7, default='OK')
    statusclass = models.CharField(max_length=13, default='table-info')


    def __str__(self):
        return self.hostname
