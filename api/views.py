import uuid
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView, ListAPIView,
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from api.permissions import IsOwner
from api.serializers import ApiKeySerializer, RegisterUserSerializer, TransactionSerializer
from transaction.models import Transaction
from user.models import UserApiKey


User = get_user_model()


class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        token, created = Token.objects.get_or_create(
            user_id=response.data["id"])
        response.data['token'] = str(token)
        return Response(response.data, status=status.HTTP_201_CREATED)


class ApiKeyView(ListCreateAPIView):
    serializer_class = ApiKeySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = UserApiKey.objects.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def post(self, request, *args, **kwargs):
        user = request.user
        platform = request.data.get('platform')
        key = UserApiKey.objects.filter(user=user).filter(platform=platform)
        if key:
            return Response(
                {'message': 'You have already Added a Key for This platform'},
                status=status.HTTP_400_BAD_REQUEST)
        return super().post(request, *args, **kwargs)


class TransactionList(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Transaction.objects.filter(user=user)
        return queryset


class ApiKeyDetail(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update or delete an API Key
    """
    permission_classes = (IsOwner,)
    queryset = UserApiKey.objects.all()
    serializer_class = ApiKeySerializer
    lookup_url_kwarg = 'key_id'


class PaymentView(APIView):
    """
    Payment View 
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """
        Receives payload to send payment request
        """
        # Setup needed request Data
        user = request.user
        reference = str(uuid.uuid4())
        platform = self.request.data.get('platform')
        self
        try:
            user_api_key = UserApiKey.objects.get(platform=platform)
            api_key = user_api_key.api_key
        except UserApiKey.DoesNotExist:
            return Response({'message': 'Please Provide a Supported Payment Platform'})
            
        gotahia_plan_id = request.data.get('plan_id')
        if gotahia_plan_id:
            try:

                amount = str(gotahia_plan.amount)
                res = PaymentProcessor().pay(
                    user=user,
                    method=source_type,
                    tx_ref=reference,
                    amount=amount,
                    plan_id=gotahia_plan_id,
                    redirect_url=get_redirect_path('seller_payment'),
                    title=settings.PAYMENT_TITLE.get("seller_title"),
                    description=settings.DESCRIPTION.get("seller_description"))
                return Response(res, status=status.HTTP_200_OK)
            except SellerPlan.DoesNotExist:
                return Response({'message': 'Plan does not exist'},
                                status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return Response({'message': 'An error occured'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'Please provide a plan id'},
                            status=status.HTTP_400_BAD_REQUEST)
