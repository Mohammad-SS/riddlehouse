from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("test", views.create_test_hour),
    path("dummy_execs", views.create_test_execs)
]
