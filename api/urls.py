from django.urls import path
from api.authentication import CustomAuthToken

from api.views import (
    ApiKeyDetail, ApiKeyView,
    RegisterUserView, TransactionList)


urlpatterns = [
    # Register
    path('user/register/', RegisterUserView.as_view(), name="register-user"),
    path('user/view-token/', CustomAuthToken.as_view(), name='token-view'),

    # Transaction List
    path('transactions/', TransactionList.as_view(), name='transaction-list'),

    # API Key
    path('user/apikeys/', ApiKeyView.as_view(), name='apikeys'),
    path('user/apikeys/<int:key_id>/',
         ApiKeyDetail.as_view(), name='apikey-detail'),


]
