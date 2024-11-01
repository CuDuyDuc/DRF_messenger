"""
ASGI config for message_be project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'message_be.settings')
django.setup()


from channels.routing import ProtocolTypeRouter, URLRouter
from message_be.apps.middleware import JWTAuthMiddleware
from message_be.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run('message_be.asgi:application', port=8080, host='0.0.0.0', reload=True)
