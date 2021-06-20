from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('show_exercise', views.show_exercise, name='show_exercise'),
    path('create_exercise', views.create_exercise, name='create_exercise'),
    path('create_menu_option', views.create_menu_option, name='create_menu_option'),
    path('logout', views.logout_user, name='logout'),
    
]