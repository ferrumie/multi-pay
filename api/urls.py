from django.urls import path

from api.views import RegisterUserView


urlpatterns = [
    # Register
    path('user/register/', RegisterUserView.as_view(), name="register-user"),


]
