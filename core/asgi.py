
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(          # AuthMiddlewareStack is just for getting access of user like self.scope['user'] in WebsocketConsumer
         URLRouter(websocket_urlpatterns)
    )
    # 'websocket': URLRouter(websocket_urlpatterns)
    
})