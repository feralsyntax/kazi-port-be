from django.urls import path
from kazi_app import views


urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register-user'),
]