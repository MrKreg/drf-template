from django.urls import path
from rest_framework.routers import DefaultRouter

from app.pkg.account.api import views


router = DefaultRouter(trailing_slash=False)
router.register(
    r'saved-address', views.SavedAddressView, basename='saved-address'
)

urlpatterns = [
    path('auth/login', views.LoginView.as_view(), name='login'),
    path('auth/signup', views.SignUpView.as_view(), name='signup'),
    path('auth/signup/confirm', views.SignUpConfirmView.as_view(), name='signup-confirm'),
    path('auth/signup/complete', views.SignUpCompleteView.as_view(), name='signup-complete'),
    path('auth/signup/social', views.SocialAuthView.as_view(), name='signup-social'),
    path('auth/reset-password', views.ResetPasswordView.as_view(), name='reset-password'),
    path('auth/reset-password/confirm', views.FinishResetPasswordView.as_view(), name='reset-password-finish'),
    path('auth/change-password', views.ChangePasswordView.as_view(), name='change-password'),
    # path('auth/change-password/confirm', views.FinishChangePasswordView.as_view(), name='change-password-finish'),
    path('auth/change-phone', views.ChangePhonedView.as_view(), name='change-phone'),
    path('auth/change-phone/confirm', views.FinishChangePhoneView.as_view(), name='change-phone-finish'),
    path('auth/profile', views.ProfileView.as_view(), name='profile'),
    path('auth/profile/photo', views.UpdateProfilePhotoView.as_view(), name='profile-photo'),
    path('auth/momo-account', views.UpdateProfileMomoView.as_view(), name='change-momo'),
    path('deauthtication', views.FacebookDataDeletionView.as_view(), name='deauthtication')
]

urlpatterns = router.urls + urlpatterns
