from django.urls import path
from rest_framework.routers import DefaultRouter

from app.pkg.account.api import views


router = DefaultRouter(trailing_slash=False)
router.register('login', views.LoginViewSet, basename='login')
router.register('signup', views.SignUpViewSet, basename='signup')
router.register('activate', views.ActivateUserViewSet, basename='activate')
router.register('password-reset', views.ResetPasswordViewSet, basename='password-reset')
router.register('change_password', views.ChangePasswordViewSet, basename='password-change')
router.register('profile', views.ProfileViewSet, basename='profile')

urlpatterns = router.urls
