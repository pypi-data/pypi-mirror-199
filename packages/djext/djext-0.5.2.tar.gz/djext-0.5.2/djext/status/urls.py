from django.urls import path

from .views import StatusView

app_name = 'status'
urlpatterns = [
    path('', StatusView.as_view(), name='view'),
]
