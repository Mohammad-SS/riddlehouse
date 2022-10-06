from django.urls import path
from . import views

app_name = "main_api"
urlpatterns = [
    path("calendar", views.GetMonthCalendar.as_view(), name="month_calendar")
]
