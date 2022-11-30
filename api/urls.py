from django.urls import path
from . import views

urlpatterns = [
    path('messages/<int:id>', views.messageReadDelete, name="message-read"),
    path('messages/', views.messagesList, name="messages"),
    path('messages/send', views.messageSend, name="message-send"),
    path('messages/unread', views.messagesUnread, name="messages-unread"),
    path('', views.apiStartPoint, name="api-overview"),
]