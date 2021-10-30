from django.urls import path

from api.views import RegisterUserView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    # Register
    path('user/register/', RegisterUserView.as_view(), name="register-user"),
    path('user/view-token/', obtain_auth_token, name='token-view')


]
