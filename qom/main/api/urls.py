from django.urls import path
from . import views

app_name = "main_api"
urlpatterns = [
    path("week" , views.GetWeekCalendar.as_view() , name="week"),
    path("calendar", views.GetMonthCalendar.as_view(), name="month_calendar"),
    path("check-coupon", views.CheckCoupon.as_view(), name="check-coupon"),

]
