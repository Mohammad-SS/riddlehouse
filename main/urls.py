from django.urls import path , include
from . import views
from .api import urls as api_urls

app_name = 'main'

urlpatterns = [
    path("api/" , include(api_urls , namespace="main_api")),
    path("" ,  views.LandingView.as_view() ,name='main'),
    path("room/<int:pk>" ,  views.RoomView.as_view() ,name='room-page')
] 
