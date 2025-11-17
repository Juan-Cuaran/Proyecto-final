from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hello/<str:username>/', views.hello, name='hello'),
    path('dashboard/', views.dashboard, name='dashboard'),
]