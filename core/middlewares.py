# middlewares.py

from django.utils import timezone
from django.core.mail import send_mail
from core.models import LoginIPAddress


class LoginNotificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            ip_address, created = LoginIPAddress.objects.get_or_create(
                user=request.user
            )

            if ip_address.last_login_ip != request.META["REMOTE_ADDR"]:
                send_mail(
                    subject="New Login Detected",
                    message=f'Your account was logged in from {request.META["REMOTE_ADDR"]} at {timezone.now()}',
                    from_email="noreply@mesika.com",
                    recipient_list=[request.user.email],
                )

            ip_address.last_login_ip = request.META["REMOTE_ADDR"]
            ip_address.save()

        response = self.get_response(request)
        return response
