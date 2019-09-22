from django.urls import path 
from . import views

app_name = 'cupons'

urlpatterns = [
    path('apply', views.CuponApply, name='apply')
]
