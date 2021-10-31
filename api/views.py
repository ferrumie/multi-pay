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
from api.serializers import ApiKeySerializer, PaymentSerializer, RegisterUserSerializer, TransactionSerializer
from api.utils.redirect import get_redirect_path
from transaction.models import Transaction
from user.models import UserApiKey
from api.payment import PaymentProcessor


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
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        """
        Receives payload to send payment request
        """
        # Setup needed request Data
        user = request.user
        reference = str(uuid.uuid4())
        data = request.data
        # load the serializer
        ser = self.serializer_class(data=data)
        if ser.is_valid():
            amount = ser.validated_data.get('amount')
            platform = ser.validated_data.get('platform').value
            description = ser.validated_data.get('description')
            logo = ser.validated_data.get('logo')
            currency = ser.validated_data.get('currency')
            title = ser.validated_data.get('title')
            print(platform)

            try:
                user_api_key = UserApiKey.objects.filter(
                    user=user).get(platform=platform)
            except UserApiKey.DoesNotExist:
                return Response({'message': 'You dont have an apikey for this platform'})
            api_key = user_api_key.api_key
            try:

                res = PaymentProcessor().pay(
                    api_key=api_key,
                    user=user,
                    method=platform,
                    tx_ref=reference,
                    amount=amount,
                    redirect_url=get_redirect_path(),
                    title=title,
                    logo=logo,
                    currency=currency,
                    description=description)
                return Response(res, status=status.HTTP_200_OK)
            except KeyboardInterrupt:
                return Response({'message': 'An error occured'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
