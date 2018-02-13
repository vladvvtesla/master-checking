from django.db import models
from django.utils import timezone

# MasterSite: MASTER-SAAO, MASTER-IAC etc
class MasterSite(models.Model):
    # author = models.ForeignKey('auth.User')
    created_date = models.DateTimeField(default=timezone.now)
    sitename = models.CharField(max_length=20)
    lat = models.CharField(max_length=20, null=True, blank=True)
    lon = models.CharField(max_length=20, null=True, blank=True)
    elev = models.CharField(max_length=20, null=True, blank=True)
    website = models.CharField(max_length=30, null=True, blank=True)

    def  sun_alt(self):
        return '45'

    def __str__(self):
        return self.sitename

# Main Server: Main Server , Ebox server 
class MainServer(models.Model):
    # author = models.ForeignKey('auth.User')
    created_date = models.DateTimeField(default=timezone.now)
    sitename = models.CharField(max_length=20)
    status = models.CharField(max_length=3, default='OK')
    ipaddr = '127.0.0.1'

    # Is ping UP?
    def  is_ping(self):
        is_ping = True
        return is_ping

    def __str__(self):
        return self.sitename
