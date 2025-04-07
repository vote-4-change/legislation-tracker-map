from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('prefs/', views.prefs, name='prefs'),
    path('manage_uploads/', views.manage_uploads, name='manage_uploads'),
]