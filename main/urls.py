from django.urls import path , include
from . import views
from .api import urls as api_urls

app_name = 'main'

urlpatterns = [
    # path("panel/", views.PanelView.as_view(), name='panel'),
    path("panel/manage-rooms", views.PanelRoomsView.as_view(), name='rooms'),
    path("panel/manage-rooms/create", views.PanelRoomView.as_view(), name='createroom'),
    path("panel/coupans", views.PanelCoupanView.as_view(), name='coupans'),
    path("panel/orders", views.PanelOrderView.as_view(), name='orders'),
  
    path("api/" , include(api_urls , namespace="main_api")),
    path("" ,  views.LandingView.as_view() ,name='main'),
    path("room/<int:pk>" ,  views.RoomView.as_view() ,name='room-page')
] 
