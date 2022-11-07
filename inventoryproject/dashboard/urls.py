from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.index, name='dashboard-index'),
    path('staff/', views.staff, name='dashboard-staff'),
    path('inventory/', views.inventoryView.as_view(), name='dashboard-inventory'),
    path('inventory/delete/<int:pk>/', views.inventory_delete, name='dashboard-inventory-delete'),              # <int:pk> shows the id of deleted item
    path('inventory/edit/<int:pk>/', views.inventory_edit, name='dashboard-inventory-edit'),              # <int:pk> shows the id of deleted item
]

# P.S. path has to be reflected also in views.py