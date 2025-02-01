from django.apps import AppConfig


class {{ project_name }}UiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{{ project_name }}_ui'
