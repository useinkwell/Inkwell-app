# class-based API views
from rest_framework.views import APIView

from .serializers import UserSerializer

# response / status
from rest_framework.response import Response
from rest_framework import status

# jwt authentication
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class Register(APIView):

    # exempt this view from using authentication/permissions
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.POST)
        data = {}

        if serializer.is_valid():
            new_user = serializer.save()

            # generate jwt access tokens for the new user
            tokens = get_jwt_access_tokens_for_user(new_user)

            data['response'] = 'Registration Successful'
            data['user_name'] = new_user.user_name
            data['email'] = new_user.email
            data['tokens'] = tokens

            return Response(data, status=status.HTTP_201_CREATED)

        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_jwt_access_tokens_for_user(user_instance):
    # generate jwt access tokens for the new user
    refresh_instance = RefreshToken.for_user(user_instance)
    tokens = {
        'refresh_token': str(refresh_instance),
        'access_token': str(refresh_instance.access_token)
    }
    return tokens
