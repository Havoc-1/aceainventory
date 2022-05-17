from django.urls import path
from . import views
from delivery.views import DeliveryRequestNew

urlpatterns = [
    path('delivery/', views.index, name='delivery-index'),
    path('delivery/past', views.past, name='delivery-past'),
    path('delivery/<int:pk>/', views.details, name='delivery-details'),
    path('delivery/approve/<int:pk>/', views.approve, name='delivery-approve'),
    path('delivery/request/', views.delivery_request, name='delivery-request'),
    path('delivery/request/new/', DeliveryRequestNew.as_view(), name='delivery-request-new'),                       
    path('delivery/edit/<int:pk>/', views.delivery_request_edit, name='delivery-request-edit'),             
    path('delivery/approve/<int:pk>/', views.delivery_request_approve, name='delivery-request-approve'),             
]