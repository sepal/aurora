from channels.routing import route
from Chat.consumers import ws_message, ws_connect, ws_disconnect, msg_consumer

channel_routing = [
    route("websocket.connect", ws_connect, path=r"^/ws/(?P<room_name>[a-zA-Z0-9_]+)$"),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
    route("chat-messages", msg_consumer),
]
