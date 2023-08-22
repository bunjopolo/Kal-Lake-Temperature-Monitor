from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('webhook/', views.webhook_handler, name='webhook_handler'),
    path('data/', views.temperature_data, name='temperature_data'),
    path('about/', views.about, name='about'),
]