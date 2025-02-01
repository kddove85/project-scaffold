from django.urls import reverse
from django.conf import settings


def login_url(request):
    return {'LOGIN_URL': settings.LOGIN_URL}

def register_url(request):
    return {'REGISTER_URL': settings.REGISTER_URL}

def logout_url(request):
    return {'LOGOUT_URL': reverse('logout')}
