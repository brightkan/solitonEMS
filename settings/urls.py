from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    # Pages
    path('', views.settings_page, name="settings_page"),
    path('add_currency/', views.add_currency, name="add_currency"),
    path('edit_currency/<int:currency_id>/', views.edit_currency_page, name="edit_currency_page"),
    path('delete_currency/<int:currency_id>/', views.delete_currency, name="delete_currency"),
]