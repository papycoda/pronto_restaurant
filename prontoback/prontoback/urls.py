from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView, name="home"),  
    path('menu/', views.MenuView, name="menu"),
    path('about/', views.AboutView, name="about"), 
    path('book/', views.BookView, name="book"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
