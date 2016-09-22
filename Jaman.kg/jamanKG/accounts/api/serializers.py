from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError,
    EmailField,
    CharField
    )

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label = "Your e-mail")
    email2 = EmailField(label = "Confirm e-mail")
    class Meta:
        model = User
        fields = [
        'username',
        'password',
        'email',
        'email2',
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                        } 

    #   Are the e-mails same
    def validate_email2(self, value):   # May be duplicated to see error message in both fields
        data = self.get_initial()
        email1 = data.get('email2')
        email2 = value
        if email1 != email2:
            raise ValidationError("The emails does not match")

        #   Checking if e-mail already registered
        user_qs = User.objects.filter(email = email2)
        if user_qs.exists():
            raise ValidationError("This e-mail address already registered")
        return value

    #   User registration with fixing password.
    #   Rewriting default create() method
    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        user_obj = User(
            username = username,
            email = email
            )
        user_obj.set_password(password)
        user_obj.save()

        return validated_data

class UserLoginSerializer(ModelSerializer):
    username = CharField(required = False, allow_blank = True)
    email = EmailField(label = "Your e-mail", required = False, allow_blank = True)
    token = CharField(allow_blank = True, read_only = True)
    class Meta:
        model = User
        fields = [
        'username',
        'password',
        'email',
        'token',
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                        } 

    #   Are the e-mails same
    def validate(self, data):
        user_obj = None
        email = data.get("email", None) #  None if not exists
        username = data.get("username", None)
        password = data["password"]
        """
        Getting the user
        """
        if not email and not username:
            raise ValidationError("Enter username or email please.")
        user = User.objects.filter(
            Q(email = email)|
            Q(username = username)
            ).distinct() # distinct() -> if there is two of the same models get the one of them...
        user = user.exclude(email__isnull = True).exclude(email__iexact = '')
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else: 
            raise ValidationError("This username/email is not valid MAN.")
        """
        Checking for password
        """
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Password you entered inncorrect. Are you hacker MeN?")

        data["token"] = "some token randomly" 
        return data