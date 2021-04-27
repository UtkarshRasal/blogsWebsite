from django.urls import path
from accounts import views
# UserListing)
from accounts import helper

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('email-verify/<str:pk>', helper.VerifyEmail.as_view(), name='email-verify'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('forgotPass/', views.ForgetPasswordView.as_view(), name='forgot-pass'),
    path('change-pass/<str:pk>', helper.ChangePasswordView.as_view()),
    path('user/', views.UserListing.as_view())
]
