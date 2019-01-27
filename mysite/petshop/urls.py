from django.urls import path

from . import views

app_name = 'petshop'

urlpatterns = [
    path('', views.index, name='index'),
    path('modify/', views.modify, name='modify'),
    path('modify/refresh/', views.index, name='refresh'),
]
