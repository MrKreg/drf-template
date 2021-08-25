from django.contrib.auth import get_user_model, authenticate, user_logged_in
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError as CoreValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from app.pkg.account.services import AuthService
from app.pkg.account.utils import get_user_token, decode_uid

User = get_user_model()


# ****************************************************************************
# COMMON PASSWORD SERIALIZER
# ****************************************************************************

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    default_error_messages = {
        'invalid_confirm': _('Passwords don\'t match.')
    }

    def validate_password(self, value):
        try:
            validate_password(value)
        except CoreValidationError as e:
            raise serializers.ValidationError(e.messages)

        return value

    def validate(self, attrs):
        attrs = super(PasswordSerializer, self).validate(attrs)
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm', None)

        if password != password_confirm:
            self.fail('invalid_confirm')

        return attrs


# ****************************************************************************
# AUTH & USER SERIALIZERS
# ****************************************************************************

class UserSerializer(serializers.ModelSerializer):
    default_error_messages = {
        'user_exists': _('User with this e-mail already exists.')
    }

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'date_joined',)
        read_only_fields = ('date_joined', 'email')


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')
    user = UserSerializer()

    class Meta:
        model = Token
        fields = ('auth_token', 'user')


# ****************************************************************************
# SIGN UP SERIALIZERS
# ****************************************************************************

class SignUpSerializer(UserSerializer, PasswordSerializer):

    def validate_email(self, value):
        value = value.lower()

        if User.objects.filter(email__iexact=value).exists():
            self.fail('user_exists')

        return value

    def create(self, validated_data):
        return AuthService.create_user(**validated_data)

    def to_representation(self, instance):
        if not instance.is_active:
            return {}
        return TokenSerializer(instance=get_user_token(instance), context=self.context).data


# ****************************************************************************
# LOGIN SERIALIZER
# ****************************************************************************

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    default_error_messages = {
        'inactive_account': _('User account is disabled.'),
        'invalid_credentials': _('Invalid credentials.'),
        'does_not_exist': _('User account with this email does not exist.'),
    }

    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            self.fail('does_not_exist')

        if not user.is_active:
            self.fail('inactive_account')

        return value

    def validate(self, attrs):
        email = attrs.get('email')

        self.user = authenticate(
            email=email,
            password=attrs.get('password')
        )

        if not self.user:
            self.fail('invalid_credentials')

        return attrs

    def create(self, validated_data):
        user_logged_in.send(
            sender=self.user.__class__,
            request=self.context.get('request'), user=self.user)
        return self.user

    def to_representation(self, instance):
        return TokenSerializer(
            instance=get_user_token(instance), context=self.context
        ).data


# ****************************************************************************
# UID & TOKEN COMMON SERIALIZER
# ****************************************************************************

class UidAndTokenSerializer(serializers.Serializer):
    code = serializers.CharField()
    user = None

    default_error_messages = {
        'invalid_code': _('Invalid code')
    }

    def validate(self, attrs):
        attrs = super(UidAndTokenSerializer, self).validate(attrs)
        raw_uid, _sep, token = attrs['code'].partition('-')

        try:
            uid = decode_uid(raw_uid)
            self.user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            self.fail('invalid_code')

        if not default_token_generator.check_token(self.user, token):
            self.fail('invalid_code')

        return attrs


# ****************************************************************************
# USER ACTIVATION EMAIL SERIALIZERS
# ****************************************************************************

class ActivateSerializer(UidAndTokenSerializer):
    default_error_messages = {
        'active_user': _('User was already activated.'),
    }

    def validate(self, attrs):
        attrs = super(ActivateSerializer, self).validate(attrs)
        if self.user.is_active:
            self.fail('active_user')
        return attrs

    def create(self, validated_data):
        return AuthService.activate(self.user)

    def to_representation(self, instance):
        return TokenSerializer(
            instance=get_user_token(self.user), context=self.context
        ).data


class ActivateRetrySerializer(serializers.Serializer):
    email = serializers.EmailField()

    default_error_messages = {
        'invalid_email': _('User with given email does not exist.'),
        'active_user': _('User with given email is already active.')
    }

    user = None

    def validate(self, attrs):
        try:
            self.user = User.objects.get(email__iexact=attrs.get('email'))
        except User.DoesNotExist:
            self.fail('invalid_email')

        if self.user.is_active:
            self.fail('active_user')

        return attrs

    def create(self, validated_data):
        AuthService.send_activation_link(self.user)
        return self.user


# ****************************************************************************
# RESET & CHANGE PASSWORD SERIALIZERS
# ****************************************************************************

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    default_error_messages = {
        'invalid_email': _('User with given email does not exist.'),
        'inactive_user': _('User with given email is not active.')
    }

    user = None

    def validate(self, attrs):
        try:
            self.user = User.objects.get(email__iexact=attrs.get('email'))
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'email': self.error_messages['invalid_email']
            })

        if not self.user.is_active:
            raise serializers.ValidationError({
                'email': self.error_messages['inactive_user']
            })
        return attrs

    def create(self, validated_data):
        AuthService.send_reset_link(self.user)
        return self.user


class FinishResetPasswordSerializer(UidAndTokenSerializer, PasswordSerializer):

    def create(self, validated_data):
        password = validated_data.get('password')
        AuthService.update_password(self.user, password)
        return self.user

    def to_representation(self, instance):
        return TokenSerializer(
            get_user_token(instance), context=self.context
        ).data


class ChangePasswordSerializer(PasswordSerializer):
    old_password = serializers.CharField(write_only=True)

    default_error_messages = {
        'wrong_password': _('Wrong old password.'),
    }

    def validate(self, attrs):
        user = authenticate(email=self.instance.email, password=attrs.get('old_password'))
        if user is None:
            self.fail('wrong_password')

        return super(ChangePasswordSerializer, self).validate(attrs)

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        AuthService.update_password(instance, password)
        return instance

    def to_representation(self, instance):
        return UserSerializer(instance, context=self.context).data
