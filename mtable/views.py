from django.shortcuts import render
from .models import MasterSite, MainServer

# Create your views here.

def main_table(request):
    master_sites = MasterSite.objects.order_by('sitename')
    return render(request, 'mtable/main_table.html', {'master_sites': master_sites})
