from django.urls import path
from . import views

urlpatterns = [
    path('<str:short_code>/', views.redirect_short_url, name='redirect'),
    path('delete/<str:short_code>/', views.delete_link, name='delete-link'),
]