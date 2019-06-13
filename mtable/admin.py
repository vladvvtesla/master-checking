from django.contrib import admin
from .models import MasterSite, MainServer, Dome, Head, Mount, Ccd, WFC, Filter, Focuser, SecondServer, Ebox, Actuator

admin.site.register(MasterSite)
admin.site.register(MainServer)
admin.site.register(Dome)
admin.site.register(Head)
admin.site.register(Mount)
admin.site.register(Ccd)
admin.site.register(WFC)
admin.site.register(Filter)
admin.site.register(Focuser)
admin.site.register(SecondServer)
admin.site.register(Ebox)
admin.site.register(Actuator)
