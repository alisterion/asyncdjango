from channels.routing import route


from asyncdjango.app.consumers import ws_connect, ws_disconnect


channel_routing = [
    route("websocket.connect", ws_connect, path=r'^/ws/'),
    route("websocket.disconnect", ws_disconnect, path=r'^/ws/'),
]
