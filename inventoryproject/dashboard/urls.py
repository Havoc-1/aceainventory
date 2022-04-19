from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.index, name='dashboard-index'),
    path('staff/', views.staff, name='dashboard-staff'),
    path('equipment/', views.equipment, name='dashboard-equipment'),
    path('deliveries/', views.deliveries, name='dashboard-deliveries'),
]

# P.S. path has to be reflected also in views.py