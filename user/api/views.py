# configuration settings
from django.conf import settings

# class-based API views
from rest_framework.views import APIView

# models
from user.models import User

# serializers
from .serializers import UserSerializer

# response / status
from rest_framework.response import Response
from rest_framework import status

# jwt authentication
from rest_framework_simplejwt.tokens import RefreshToken # new access token
from rest_framework_simplejwt.tokens import AccessToken # verify access token
from rest_framework_simplejwt.exceptions import InvalidToken # exception

# for cryptographic encryption and decryption
from cryptography.fernet import Fernet
encryption_key = settings.CRYPTOGRAPHY_KEY.encode()
encryption_handler = Fernet(encryption_key)

# others
from user.email_sender import send_email


def verify_token(token):
    try:
        access_token = AccessToken(token)
        return access_token.payload
    except InvalidToken:
        return None


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

            # encrypt access token for sending in verification URL
            encrypted_access_token = \
                encryption_handler.encrypt(tokens['access_token'].encode())

            # send account confirmation email with user verification URL
            send_email(
                'Inkwell Email Verification',
                f'''
                Click this link to activate your Inkwell account:
                http://127.0.0.1:8000/auth/verify/?x_access_token={encrypted_access_token.decode()}/
                ''',
                'no-reply@inkwellteam.com',
                new_user.email
            )


            return Response(data, status=status.HTTP_201_CREATED)

        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(APIView):
    '''when a user clicks the verification link in the email, this is the
    view that handles the verification and subsequent redirection.'''

    # exempt this view from using authentication/permissions
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        # the encrypted access token is received here and decoded
        encrypted_access_token = \
            self.request.GET.get('x_access_token').replace('/','').encode()
        access_token = \
            encryption_handler.decrypt(encrypted_access_token).decode()

        token_user_data = verify_token(access_token)
        if token_user_data:
            user = User.objects.get(id=token_user_data['user_id'])
            user.is_active = True
            user.save()
            
            return Response({user.user_name: "Verified"}, 
                            status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    
class ForgotPassword(APIView):
    '''this view collects the user email and sends an email to it containing
    the url for password reset'''

    # exempt this view from using authentication/permissions
    permission_classes = []
    authentication_classes = []

    def post(self, request):

        user_email = self.request.POST.get('email')
        user = User.objects.filter(email=user_email).first()
        if user:
        
            # generate fresh jwt access token for user
            access_token = get_jwt_access_tokens_for_user(user)['access_token']

            # encrypt access token for sending in password reset URL
            encrypted_access_token = \
                encryption_handler.encrypt(access_token.encode())

            # send password reset email with user password reset URL
            send_email(
                'Inkwell Password Reset',
                f'''
                Click this link to reset your Inkwell password:
                http://127.0.0.1:8000/auth/reset_password/?x_access_token={encrypted_access_token.decode()}/
                ''',
                'no-reply@inkwellteam.com',
                user_email
            )
            print(f'\n\nPASSWORD RESET TOKEN:{encrypted_access_token.decode()}\n\n')
            return Response(status=status.HTTP_200_OK)
            
        return Response(status=status.HTTP_404_NOT_FOUND)


class ResetPassword(APIView):
    '''when a user clicks the password reset link in the email, this is the
    view that handles the password reset and subsequent redirection.'''

    # exempt this view from using authentication/permissions
    permission_classes = []
    authentication_classes = []

    
    def get_user(self):
        # the encrypted access token is received here and decoded
        encrypted_access_token = \
            self.request.GET.get('x_access_token').replace('/','').encode()
        access_token = \
            encryption_handler.decrypt(encrypted_access_token).decode()

        token_user_data = verify_token(access_token)
        if token_user_data:
            user = User.objects.get(id=token_user_data['user_id'])
            return user
        return None


    def post(self, request):
        password = self.request.POST.get('password')
        password2 = self.request.POST.get('password2')
        user = self.get_user()

        if user and password == password2:
            user.set_password(password)
            user.save()
            
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)





def get_jwt_access_tokens_for_user(user_instance):
    # generate jwt access tokens for the new user
    refresh_instance = RefreshToken.for_user(user_instance)
    tokens = {
        'refresh_token': str(refresh_instance),
        'access_token': str(refresh_instance.access_token)
    }
    return tokens
