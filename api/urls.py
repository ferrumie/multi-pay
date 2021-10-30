from django.urls import path
from api.authentication import CustomAuthToken

from api.views import RegisterUserView


urlpatterns = [
    # Register
    path('user/register/', RegisterUserView.as_view(), name="register-user"),
    path('user/view-token/', CustomAuthToken.as_view(), name='token-view'),


]
