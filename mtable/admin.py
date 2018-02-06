from django.contrib import admin
from .models import CellValue, MasterSite, MainServer

admin.site.register(CellValue)
admin.site.register(MasterSite)
admin.site.register(MainServer)
