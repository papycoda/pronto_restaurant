from django.contrib import admin
from django.urls import path
from Home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.HomePageView, name="home"),  
    path('menu/', views.MenuView, name="menu"),
    path('about/', views.AboutView, name="about"), 
    path('book/', views.BookView, name="book"),
]
