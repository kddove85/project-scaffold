from django.urls import path, re_path
from .views import IndexView

app_name = '{{ project_name }}_ui'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    re_path(r'^.*$', IndexView.as_view())
]