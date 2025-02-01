from django.urls import reverse
from django.conf import settings


def spa_context(request):
    user_info = {
        'id': request.user.pk,
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    } if request.user.is_authenticated else None

    return {
        'spa_context': {
            'user': user_info,
            'register_url': settings.REGISTER_URL,
            'login_url': settings.LOGIN_URL,
            'logout_url': reverse('logout')
        }
    }
