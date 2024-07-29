from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.urls import re_path as url
from django.views.i18n import JavaScriptCatalog
from django.conf.urls.static import static
from Home import views


js_info_dict = {
    'packages': ('recurrence', ),
}

admin.site.site_header = "Pronto Admin Panel"
admin.site.site_title = "Pronto Admin Panel"
admin.site.index_title = "Welcome to Pronto Admin"

urlpatterns = [
    path('5y5adm1n776686/', admin.site.urls),
    path('', views.HomePageView, name="home"),  
    path('menu/', views.MenuView, name="menu"),
    path('about/', views.AboutView, name="about"), 
    path('book/', views.BookView, name="book"),
    path('import/', views.import_from_excel, name='import_from_excel'),
    path('events/', views.event_list, name='events'),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), js_info_dict),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
