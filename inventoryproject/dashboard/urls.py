from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.index, name='dashboard-index'),
    path('adash/', views.admin_dashboard, name='dashboard-admin'),
    path('update-user-location/<int:user_id>/', views.update_user_location, name='update-user-location'),
    path('inventory/', views.inventoryView.as_view(), name='dashboard-inventory'),
    path('deliveries/', views.DeliveryList.as_view(), name='list-deliveries'),
    path('create/', views.delivery_create_view, name='create-delivery'),
    path('deliveries/<int:pk>/', views.delivery_batch_details, name='delivery_details'),
    path('deliveries/quotation/<int:pk>/',views.QuotationList.as_view(), name='list-quotations'),
    path('deliveries/quotation/<int:pk>/create', views.quotation_create_view, name='create-quotation'),
    path('deliveries/quotation/<int:pk>/<int:pk2>', views.quotation_details, name='quotation_details'),
    path('approveDelivery',views.approveDelivery, name ='approveDelivery'),
    path('arriveDelivery',views.arriveDelivery, name ='arriveDelivery'),
]
# P.S. path has to be reflected also in views.py