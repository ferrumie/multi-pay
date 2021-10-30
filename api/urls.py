from django.urls import path
from api.authentication import CustomAuthToken

from api.views import RegisterUserView, TransactionList


urlpatterns = [
    # Register
    path('user/register/', RegisterUserView.as_view(), name="register-user"),
    path('user/view-token/', CustomAuthToken.as_view(), name='token-view'),

    # Transaction List
    path('transactions/', TransactionList.as_view(), name='transaction-list')


]
