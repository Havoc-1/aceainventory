from django.shortcuts import render
from django.http import HttpResponse

# P.S. path has to be reflected also in urls.py
def index(request):
    return render(request, 'dashboard/index.html')

def staff(request):
    return render(request, 'dashboard/staff.html')

def equipment(request):
    return render(request, 'dashboard/equipment.html')

def deliveries(request):
    return render(request, 'dashboard/deliveries.html')