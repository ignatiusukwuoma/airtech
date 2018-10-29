from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking, name='booking'),
    path('profile/', views.profile, name='profile'),
    path('delete_passport/', views.delete_passport, name='delete_passport'),
    path('summary/', views.summary, name='summary'),
    path('payment/', views.payment, name='payment'),
    path('success/', views.success, name='success')
]
