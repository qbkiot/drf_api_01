from django.urls import path, include, re_path
from . import views
from rest_framework import routers
from .views import SubItemsView, ItemsView, RemindersView, PetsView

router = routers.DefaultRouter()
router.register('items', views.ItemsView, basename='items')
router.register('subitems', views.SubItemsView, basename='subitems')
router.register('pets', views.PetsView, basename='pets')
router.register('reminders', views.RemindersView, basename='reminders')

urlpatterns = [
    
    re_path('', include(router.urls)),
    #path('items/', ItemsView.as_view()),
    #path('subitems/', SubItemsView.as_view()),
    path('getdata/', views.getData),
    path('login/', views.login),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    #path('add/', views.addItem),
    #path("add/", views.ItemView.as_view(), name="additem"),
    path('<str:name>/delete/', views.deleteItem),
    path('<str:name>/update/', views.editItem),
    path('deleteall/', views.deleteAll),
    path('addpet/', views.add_pet),
    path('getpets/', views.getPets),
    path('appendreminder/', views.appendReminder),
    
]