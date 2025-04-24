from django.contrib import admin
from django.urls import path, include
from shortener.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('', include('user.urls')),
    path('', include('shortener.urls')),
]
