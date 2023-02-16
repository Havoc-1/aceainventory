from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.index, name='dashboard-index'),
    path('staff/', views.staff, name='dashboard-staff'),
    path('inventory/', views.inventoryView.as_view(), name='dashboard-inventory'),
    path('deliveries/', views.DeliveryList.as_view(), name='list-deliveries'),
    path('create/', views.delivery_create_view, name='create-delivery'),
    # path('update/<int:pk>/', views.DeliveryUpdate.as_view(), name='update-delivery'),
    path('deliveries/<int:pk>/', views.delivery_batch_details, name='delivery_details'),
    path('approveDelivery',views.approveDelivery, name ='approveDelivery'),
    path('arriveDelivery',views.arriveDelivery, name ='arriveDelivery'),
]
# P.S. path has to be reflected also in views.py