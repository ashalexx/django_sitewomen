from django.contrib import admin
from django.urls import path
from women import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('women/', views.index),
    path('cats/', views.categories),
]