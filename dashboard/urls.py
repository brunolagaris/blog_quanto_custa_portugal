from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='dashboard_index'),
    path('ads/', views.index, name='ads_index'),
    path('articles/', views.index, name='articles_index'),
    path('calcuators/', views.index, name='calculators_index'),
    path('users', views.index, name='users_index'),
    path('settings', views.index, name='settings_index'),
]