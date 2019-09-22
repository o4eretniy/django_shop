from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.OrderCreate, name='OrderCreate'),
    path('admin/order/<order_id>/', views.AdminOrderDetail, name='AdminOrderDetail'),
    path('admin/order/<order_id>/pdf/', views.AdminOrderPDF, name='AdminOrderPDF')
]
