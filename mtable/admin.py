from django.contrib import admin
from .models import MasterSite, MainServer, Head, Mount

admin.site.register(MasterSite)
admin.site.register(MainServer)
admin.site.register(Head)
admin.site.register(Mount)
