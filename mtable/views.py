from django.shortcuts import render
from .models import CellValue, MasterSite, MainServer

# Create your views here.

def main_table(request):
    main_servers = MainServer.objects.order_by('sitename')
    return render(request, 'mtable/main_table.html', {'main_servers': main_servers})
