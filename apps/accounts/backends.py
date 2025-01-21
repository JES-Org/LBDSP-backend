from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomBackend(ModelBackend):
    print("calling backend auth")

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        print("calling backend auth")

        # Try to find user by email or phone_number
        user = None
        if username:
            try:
                # Check if it's an email or phone number
                if '@' in username:  # Likely an email
                    user = UserModel.objects.get(email=username)
                else:  # Likely a phone number
                    user = UserModel.objects.get(phone_number=username)
            except UserModel.DoesNotExist:
                return None

        if user and user.check_password(password):
            return user
        return None
    
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
