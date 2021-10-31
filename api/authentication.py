from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from api.serializers import MyAuthTokenSerializer


class CustomAuthToken(ObtainAuthToken):
    serializer_class = MyAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        response = {
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'phone_number': str(user.phone_number)
        }
        return Response(response, status=status.HTTP_200_OK)
