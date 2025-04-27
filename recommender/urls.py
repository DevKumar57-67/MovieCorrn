from django.urls import path
from django_project import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recommend/', views.recommend, name='recommend'),
]
