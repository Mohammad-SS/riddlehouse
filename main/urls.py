from django.urls import path , include
from . import views
from .api import urls as api_urls
urlpatterns = [
    path("api/" , include(api_urls , namespace="main_api"))
]
