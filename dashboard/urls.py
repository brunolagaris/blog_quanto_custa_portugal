from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='dashboard_index'),
    path('ads/', views.index, name='ads_index'),
    path('articles/', views.articles_list, name='articles_list'),
    path('articles/new', views.article_create, name='article_create'),
    path('articles/<int:pk>/edit/', views.article_edit, name='article_edit'),
    path('articles/<int:pk>/delete/', views.article_delete, name='article_delete'),
    path('calcuators/', views.index, name='calculators_index'),
    path('users', views.index, name='users_index'),
    path('settings', views.index, name='settings_index'),
]