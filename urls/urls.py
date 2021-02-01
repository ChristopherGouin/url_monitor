# coding: UTF-8
from django.urls import path

from urls import views
from urls import cbv

app_name = 'urls'
urlpatterns = [
    path('', views.urls_list, name="urls_list"),
    path('new_url/', cbv.UrlCreateView.as_view(), name="new_url"),
    path('delete_url-<int:pk>/', cbv.UrlDeleteView.as_view(), name="delete_url"),
    path('update_url-<int:pk>/', cbv.UrlUpdateView.as_view(), name="update_url"),
]