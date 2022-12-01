from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('add/', views.addItem),
    path('<str:name>/delete/', views.deleteItem),
    path('<str:name>/update/', views.editItem),
    path('deleteall/', views.deleteAll),
]