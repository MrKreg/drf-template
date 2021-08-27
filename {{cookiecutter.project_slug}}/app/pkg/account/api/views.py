from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, viewsets, mixins as drf_mixins, status
from rest_framework.decorators import action

from app.pkg.account.api import serializers
from app.pkg.common.mixins import ActionMixin

User = get_user_model()


class SignUpViewSet(drf_mixins.CreateModelMixin, ActionMixin, viewsets.GenericViewSet):
    serializer_class = serializers.SignUpSerializer


class ActivateUserViewSet(drf_mixins.CreateModelMixin, ActionMixin, viewsets.GenericViewSet):
    serializer_class = serializers.ActivateSerializer

    @action(detail=False, methods=('POST',), serializer_class=serializers.ActivateRetrySerializer)
    def retry(self, request, *args, **kwargs):
        return self.list_action(request, *args, **kwargs)


class LoginViewSet(drf_mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.LoginSerializer


class ResetPasswordViewSet(drf_mixins.CreateModelMixin, ActionMixin, viewsets.GenericViewSet):
    serializer_class = serializers.ResetPasswordSerializer

    @action(detail=False, methods=('POST',), serializer_class=serializers.FinishResetPasswordSerializer)
    def finish(self, request, *args, **kwargs):
        return self.list_action(request, *args, **kwargs)


class ChangePasswordViewSet(drf_mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ProfileViewSet(drf_mixins.RetrieveModelMixin, drf_mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
