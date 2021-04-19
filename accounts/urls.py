from django.urls import path
from .views import RegisterView, LoginView, ForgetPasswordView
# UserListing)
from .helper import VerifyEmail, ChangePasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('email-verify/<str:pk>', VerifyEmail.as_view(), name='email-verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgotPass/', ForgetPasswordView.as_view(), name='forgot-pass'),
    path('change-pass/<str:pk>', ChangePasswordView.as_view()),
    # path('user/', UserListing.as_view())
]
