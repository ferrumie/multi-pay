import uuid
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView, ListAPIView,
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from api.permissions import IsOwner
from api.processor import PaymentProcessor
from api.serializers import (
    ApiKeySerializer, PaymentSerializer,
    RegisterUserSerializer, TransactionSerializer)
from api.utils.redirect import get_redirect_path
from transaction.models import Transaction
from user.models import UserApiKey


# Get user model
User = get_user_model()


class RegisterUserView(CreateAPIView):
    '''
    POST: Create a user, api_key is generated for auth
    req data:
    {
         email:e@e.com,
         password: wdwk,
         password2: wkj,
         phone_number: +2348063133959
    }
    '''
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Create token and store in response
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
        ''' Assign user by default from request while creatingg APIKey'''
        user = self.request.user
        serializer.save(user=user)

    def post(self, request, *args, **kwargs):
        user = request.user
        platform = request.data.get('platform')
        key = UserApiKey.objects.filter(user=user).filter(platform=platform)
        # TODO: encrypt API keys before storing in db to make it safer

        # Check if an api key exist for the platform. for this logged in user
        if key:
            return Response(
                {'message': 'You have already Added a Key for This platform'},
                status=status.HTTP_400_BAD_REQUEST)
        return super().post(request, *args, **kwargs)


class TransactionList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user = self.request.user

        # Only return transaction for the logged in user
        queryset = Transaction.objects.filter(user=user)
        return queryset


class ApiKeyDetail(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update or delete an API Key
    """
    permission_classes = (IsOwner,)
    queryset = UserApiKey.objects.all()
    serializer_class = ApiKeySerializer

    # set a custom lookup id
    lookup_url_kwarg = 'key_id'


class PaymentView(APIView):
    """
    Payment View
    This is where most of the calls take place
    POST
    request {
        'amount': 'required',
        'platform': required,
        title: provisionally required
    }
    The authenticated user supplies a platform, the api_key is retrieved
    then the payment processor takes in the params and transfer the request 
    to the specific payment function.
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
            platform = ser.validated_data.get('platform')
            description = ser.validated_data.get('description')
            logo = ser.validated_data.get('logo')
            currency = ser.validated_data.get('currency')
            title = ser.validated_data.get('title')

            try:
                user_api_key = UserApiKey.objects.filter(
                    user=user).get(platform=platform[0])
            # if apikey for the specified platform does not exist
            # return an error
            except UserApiKey.DoesNotExist:
                return Response({'message': 'You dont have an apikey for this platform'}, status=status.HTTP_400_BAD_REQUEST)

            api_key = user_api_key.api_key

            # Call the payment processor with payload
            res = PaymentProcessor().pay(
                api_key=api_key,
                user=user,
                method=platform[1],
                tx_ref=reference,
                amount=amount,
                redirect_url=get_redirect_path(),
                title=title,
                logo=logo,
                currency=currency,
                description=description)
            response = Response(res, status=status.HTTP_200_OK)\

            # set up cookie with platform list
            # when redirect url is called, this cookie is checked
            # to make the view call the correct function for the platform
            response.set_cookie(
                'platform', [platform[0], platform[1]])
            return response

        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentConfirmationView(APIView):
    """
    Confirms if the payment is successful
    Redirect url view, for the platforms
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        Redirect View for the confirmation of the payment        
        """

        user = request.user
        transaction_ref = request.GET.get('tx_ref')
        transaction_id = request.GET.get('transaction_id')

        # Read the plaform from the cookie
        platform = request.COOKIES['platform']

        # Convert the string to a list
        platform = eval(platform)
        method = platform[1]
        # Get the API key
        try:
            user_api_key = UserApiKey.objects.filter(
                user=user).get(platform=platform[0])
        except UserApiKey.DoesNotExist:
            return Response({'message': 'You dont have an apikey for this platform'})
        api_key = user_api_key.api_key
        res = PaymentProcessor().verify(
            transaction_id=transaction_id,
            method=method, user=user, api_key=api_key,
            transaction_ref=transaction_ref)
        if res['status'] == 'success':
            return Response(res, status=status.HTTP_200_OK)
        else:
            return Response({'message': res['message']}, status=status.HTTP_400_BAD_REQUEST)
