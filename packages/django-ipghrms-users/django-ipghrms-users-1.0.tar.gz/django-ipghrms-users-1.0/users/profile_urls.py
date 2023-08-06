from django.urls import path
from . import views

urlpatterns = [
	path('profile/', views.ProfileDetail, name="user-profile"),
]


