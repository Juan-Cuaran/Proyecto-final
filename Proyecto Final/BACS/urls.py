"""
URL configuration for BACS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from core import views
from visitors import views as visitors_views
from credentials import views as credentials_views
from accesscontrol import views as accesscontrol_views
from reports import views as reports_views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('visitors/create/', visitors_views.create_visitor, name='create_visitor'),
    path('visitors/list/', visitors_views.list_visitor, name='list_visitor'),
    path('visitors/restrict/', visitors_views.restrict_visitor, name='restrict_visitor'),
    path('credentials/create/', credentials_views.Asign_credential, name='create_credential'),
    path('accesscontrol/', RedirectView.as_view(pattern_name='create_access_event', permanent=False)),
    path('accesscontrol/create/', accesscontrol_views.create_access_event, name='create_access_event'),
    path('accesscontrol/reports/', accesscontrol_views.create_reports, name='create_reports'),
    path('reports/', reports_views.list_reports, name='reports_list'),
    path('reports/<int:pk>/', reports_views.report_detail, name='report_detail'),
    ]
