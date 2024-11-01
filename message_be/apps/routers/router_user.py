from message_be.apps.routers import RegisterView, LoginAPIView, path

urlpatterns = [
    path('register-user/', RegisterView.as_view(), name='register-user'),
    path('login-user/', LoginAPIView.as_view(), name='login-user'),
]