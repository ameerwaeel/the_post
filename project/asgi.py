import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns  # مسار app اللي فيه الشات

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'the_post.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
