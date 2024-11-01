from django.urls import path, include

urlpatterns = [
    path('user/', include('message_be.apps.routers.router_user')),
]