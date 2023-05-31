from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.index, name='dashboard-index'),
    path('adash/', views.admin_dashboard, name='dashboard-admin'),
    path('update-user-group/<int:user_id>/', views.update_user_groups, name='update-user-groups'),
    path('update-user-location/<int:user_id>/', views.update_user_location, name='update-user-location'),
    path('update_inventory_restocking/<int:inventory_id>/', views.update_inventory_restocking, name='update-inventory-restocking'),
    path('inventory/', views.inventoryView.as_view(), name='dashboard-inventory'),
    path('inventory/edit', views.edit_inventory, name='edit_inventory'),
    path('inventory/withdraw/', views.inventory_withdraw, name='inventory_withdraw'),
    path('inventory/withdrawals/', views.inventory_withdrawals, name='inventory_withdrawals'),
    path('deliveries/', views.DeliveryList.as_view(), name='list-deliveries'),
    path('requests/', views.RequestList.as_view(), name='list-requests'),
    path('create/', views.createRequest, name='create-request'),
    path('create_delivery', views.create_delivery, name='set-delivery'),
    path('requests/quotation/<int:pk>/',views.QuotationList.as_view(), name='list-quotations'),
    path('requests/quotation/<int:pk>/partial',views.create_partial_delivery, name='create-partial-delivery'),
    path('requests/quotation/<int:pk>/create', views.quotation_create_view, name='create-quotation'),
    path('requests/quotation/<int:pk>/edit', views.edit_quotation, name='edit_quotation'),
    path('requests/quotation/<int:pk>/delete', views.delete_quotation, name='delete_quotation'),
    path('requests/quotation/<int:pk>/details', views.quotation_details, name='quotation_details'),
    # path('approvePurchaseRequest',views.approvePurchaseRequest, name ='approvePurchaseRequest'),
    path('arriveDelivery',views.arriveDelivery, name ='arriveDelivery'),
    path('approveQuotation',views.approveQuotation, name ='approveQuotation'),
]
# P.S. path has to be reflected also in views.py