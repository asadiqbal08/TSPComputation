from django.urls import path

# importing views from views..py
from .views import PublishMessages

urlpatterns = [
	path(r'', PublishMessages.as_view(), name='index'),
	path(r'publish/', PublishMessages.as_view(), name='publish'),
]
