from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from api.serializers import AddApiKeySerializer, RegisterUserSerializer, TransactionSerializer
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


class AddApiKeyView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AddApiKeySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = UserApiKey.objects.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class TransactionList(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Transaction.objects.filter(user=user)
        return queryset


class PaymentView(APIView):
    """
    Payment View 
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """
        Receives payload to send payment request
        """
        user = request.user
        reference = str(uuid.uuid4())
        source_type = self.request.data.get('source_type')
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
