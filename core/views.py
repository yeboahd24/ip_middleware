from rest_framework import views, permissions
from rest_framework.response import Response
from rest_framework import status
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework_simplejwt.views import TokenObtainPairView
from django_otp.plugins.otp_static.models import StaticDevice
from django_otp.plugins.otp_static.models import StaticToken
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


def get_user_totp_device(self, user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device


class TOTPCreateView(views.APIView):
    """
    Use this endpoint to set up a new TOTP device
    This enable the 2fa and generat qrcode
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        device = get_user_totp_device(self, user)
        if not device:
            device = user.totpdevice_set.create(confirmed=False)
        url = device.config_url
        return Response(url, status=status.HTTP_201_CREATED)


class TOTPVerifyView(views.APIView):
    """
    Use this endpoint to verify/enable a TOTP device
    This takes in the 6 digit code from authentication app and verify it
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, token, format=None):
        user = request.user
        device = get_user_totp_device(self, user)
        if not device == None and device.verify_token(token):
            if not device.confirmed:
                device.confirmed = True
                device.save()
            return Response(True, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    # Customize the response data, if needed
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Add custom data to the response, if desired
        return response


def get_user_static_device(self, user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, StaticDevice):
            return device


class StaticCreateView(views.APIView):
    """
    Use this endpoint to create static recovery codes.
    Generate recovery code and save it securely somewhere
    """

    permission_classes = [permissions.IsAuthenticated]
    number_of_static_tokens = 6

    def get(self, request, format=None):
        device = get_user_static_device(self, request.user)
        if not device:
            device = StaticDevice.objects.create(user=request.user, name="Static")

        device.token_set.all().delete()
        tokens = []
        for n in range(self.number_of_static_tokens):
            token = StaticToken.random_token()
            device.token_set.create(token=token)
            tokens.append(token)

        return Response(tokens, status=status.HTTP_201_CREATED)


class StaticVerifyView(views.APIView):
    """
    Use this endpoint to verify a static token.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, token, format=None):
        user = request.user
        device = get_user_static_device(self, user)
        print(device == None)
        if not device == None and device.verify_token(str(token)):
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TOTPDeleteView(views.APIView):
    """
    Use this endpoint to delete a TOTP device
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        devices = devices_for_user(user)
        for device in devices:
            device.delete()
        user.save()
        return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def update_user_ip(request):
    user = request.user
    user.last_login_ip = request.META["REMOTE_ADDR"]
    user.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(request, username=username, password=password)

    if user is not None:
        # Login successful

        return Response({"success": "Login successful"})
    else:
        # Login failed
        return Response({"error": "Invalid credentials"}, status=400)
