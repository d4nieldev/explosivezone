from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('אימונים מועדפים', views.favorites, name='favorites'),
    path('אימון/<str:exercise_title>/', views.show_exercise, name='show_exercise'),
    path('אימון חדש/<str:exercise_title>/', views.create_exercise, name='create_exercise'),
    path('create_menu_option', views.create_menu_option, name='create_menu_option'),
    path('logout', views.logout_user, name='logout'),
    path('fav', views.fav, name='fav'),
    path('discard_page', views.discard_page, name='discard_page')
    
]