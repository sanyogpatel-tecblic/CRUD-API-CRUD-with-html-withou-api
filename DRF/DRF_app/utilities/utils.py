from DRF_app.customs.authentication import create_refresh_token,decode_refresh_token,create_access_token
from django.core.mail import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()
def get_tokens_for_user(user):
    # refresh = RefreshToken.for_user(user)
    # access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    id = decode_refresh_token(refresh_token)
    refresh_access_token = create_access_token(user.id)

    return {
        "refresh": refresh_token,
        "access": refresh_access_token,
    }

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["subject"],
            body=data["body"],
            from_email=os.getenv("EMAIL_HOST_USER"),
            to=[data["to_email"]],
        )
        print(email)
        email.send()
