from django.conf.urls import handler404
from django.contrib import admin
from django.urls import path, include
from django.views.defaults import page_not_found

from women import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),
]


handler404 = page_not_found