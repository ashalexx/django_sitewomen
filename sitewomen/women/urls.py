from django.urls import path
from women import views

urlpatterns = [
    path('', views.index),
    path('cats/<int:cat_id>/', views.categories),
    path('cats/<slug:cat_slug>/', views.categories_by_slug),
]
