"""proyect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from subscribers.views import SubscriberListView,import_csv,export_csv
from django.shortcuts import redirect

urlpatterns = [     
     #Path to root added for demonstration purposes
     path('', lambda request: redirect('subscriberListView', permanent=False)),
     path('admin/subscribers', SubscriberListView.as_view(), name='subscriberListView'),
     path('admin/import_csv', import_csv, name='import_csv'),
     path('admin/export_csv', export_csv, name='export_csv'),
]
