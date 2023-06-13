from django.urls import path

from .views import RegisterApiView, VerifyEmailApiView, LoginApiView, CreateUserProfileApiView

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name='register'),
    path('verify_email/', VerifyEmailApiView.as_view(), name='verify_email'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('user_info/', CreateUserProfileApiView.as_view(), name='user_info'),
]
