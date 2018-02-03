from django.shortcuts import render

# Create your views here.

def main_table(request):
    return render(request, 'mtable/main_table.html', {})
