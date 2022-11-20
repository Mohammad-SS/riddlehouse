from django.urls import path , include
from . import views
from .api import urls as api_urls

app_name = 'main'

urlpatterns = [
    path("api/", include(api_urls, namespace="main_api")),

    path("login", views.LoginView.as_view(), name='login'),
    path("panel/", views.LoginView.as_view(), name='panel'),
    path("panel/manage-rooms", views.PanelRoomsView.as_view(), name='rooms'),
    path("panel/manage-rooms/create", views.PanelRoomView.as_view(), name='createroom'),
    path("panel/manage-rooms/edit/<int:pk>", views.PanelRoomEditView.as_view(), name='editroom'),

    path("panel/coupans", views.PanelCoupanView.as_view(), name='coupans'),
    path("panel/coupans/<int:pk>/remove", views.RemoveCoupon.as_view(), name='remove-coupon'),

    path("panel/orders", views.PanelOrderView.as_view(), name='orders'),

    path("panel/schedule", views.PanelScheduleView.as_view(), name='schedule'),
    path("panel/schedule/<int:pk>/remove" , views.PanelRemoveSchedule.as_view() , name="remove-schedule"),
    
    path("panel/settings", views.PanelSettingsView.as_view(), name='settings'),

    path("" ,  views.LandingView.as_view() ,name='main'),
    path("اتاق-های-فرار/<str:slug>" ,  views.RoomView.as_view() ,name='room-page'),
    path("reserve-completed", views.ReserveCompleted.as_view(), name='reserved-page')

] 
