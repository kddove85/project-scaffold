from django.urls import include, path
from .import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register_page, name='register'),
]
