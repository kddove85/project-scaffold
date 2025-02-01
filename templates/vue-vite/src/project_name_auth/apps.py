from django.apps import AppConfig


class {{ project_name }}AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{{ project_name }}_auth'
