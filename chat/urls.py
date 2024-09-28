
from django.urls import path
from chat.views import *

urlpatterns = [
    path('', index_view, name='chat_index'),
    path('<str:room_name>', room_view, name='chat_room'),
    path('pm/<str:username>', private_room_view, name='private_chat_room'),
    # path('chatwindow/<str:room_name>', partial_chatwindow_view, name='partial_chat_window'),
]
