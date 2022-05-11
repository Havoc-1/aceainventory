from django.urls import path
from . import views

urlpatterns = [
    path('delivery/', views.index, name='delivery-index'),
    path('delivery/#/', views.details, name='delivery-details'),
    path('delivery/request/', views.delivery_request, name='delivery-request'),
    path('delivery/request/new/', views.delivery_request_new, name='delivery-request-new'),              
    path('delivery/edit/#/', views.delivery_request_edit, name='delivery-request-edit'),             
]