from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('show_exercise', views.show_exercise, name='show_exercise')
]