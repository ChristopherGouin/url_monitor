# coding: UTF-8
from django.urls import path

from verifications import views

app_name = 'verifications'
urlpatterns = [
    path('verifications-url-<int:url_id>/', views.verification_list, name="verifications_list")
]