"""cmdb_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, handler404
from django.conf import settings
from django.contrib import admin
from cmdb import views
from django.views.static import serve
handler404 = views.page_not_found
urlpatterns = [
    url(r'^static/(?P<path>.*)$',serve,{'document_root': settings.STATIC_ROOT,}),
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^asset_info.html', views.asset_info),
    url(r'^asset/', views.asset_info),
    url(r'^asset_api/', views.asset_api),
    url(r'^asset_add/', views.asset_add),
    url(r'^asset_edit/(\d+)', views.asset_edit),
    url(r'^asset_delete/(\d+)', views.asset_delete, name="asset_delete"),
    url(r'^asset_details/(\d+)', views.asset_details),
    url(r'^$', views.asset_info),
    url(r'^asset_export', views.export_excel),

]


