from django.urls import path
from .views import ChatRoomView, ClientChatView

app_name = 'chat'

urlpatterns = [
    path("chat/", ChatRoomView.as_view(), name="chat_room"),
    path("chat/client/<int:client_id>/", ClientChatView.as_view(), name="chat_with_client"),
]
