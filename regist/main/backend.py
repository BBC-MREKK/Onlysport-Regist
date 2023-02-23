from allauth.account.auth_backends import AuthenticationBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
import phonenumbers

UserModel = get_user_model()


class PhoneNumberBackend(AuthenticationBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            phone_number = phonenumbers.parse(username, None)
            if not phonenumbers.is_valid_number(phone_number):
                return None
        except phonenumbers.phonenumberutil.NumberParseException:
            return None

        user = UserModel.objects.filter(Q(phone_number__iexact=username) | Q(phone_number_verified__iexact=username)).first()

        if user is None:
            return None

        if not user.check_password(password):
            return None

        return user