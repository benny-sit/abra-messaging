from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Message
from .serializers import MessagesSerializer, SendMessageSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from django.contrib.auth import get_user_model

UserModel = get_user_model()


@api_view(['GET'])
@permission_classes([AllowAny])
def apiStartPoint(req):
    return Response("API BASE POINT")


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def messagesList(req):
    sender = UserModel.objects.get(username=req.user.username)
    query = (Q(sender=sender.id) & Q(sender_deleted=False)) | (Q(receiver=sender.id) & Q(receiver_deleted=False))
    messages = Message.objects.filter(query).order_by('-sent_at')

    serializer = MessagesSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['GET', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def messageReadDelete(req, id):
    sender = UserModel.objects.get(username=req.user.username)
    if not Message.objects.filter(pk=id).exists():
        return Response({"error": "Message Does Not Exists"}, status=status.HTTP_400_BAD_REQUEST)
    message = Message.objects.get(pk=id)

    if sender.id != message.sender.id and sender.id != message.receiver.id:
        return Response({"error": "Unauthorized to this message"}, status=status.HTTP_403_FORBIDDEN)

    if req.method == 'GET':
        if sender.id == message.receiver.id:
            message.read = True
            message.save()
        serializer = MessagesSerializer(message)
        return Response(serializer.data)

    elif req.method == 'DELETE':
        if sender.id == message.receiver.id:
            message.receiver_deleted = True
        elif sender.id == message.sender.id:
            message.sender_deleted = True

        if message.receiver_deleted and message.sender_deleted:
            message.delete()
        else:
            message.save()

        return Response({"success": f'Deleted Message with id={id}'}, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def messageSend(req):
    if 'receiver' not in req.data:
        return Response({"error": "You Need To Specify Message Receiver"}, status=status.HTTP_400_BAD_REQUEST)
    message = req.data
    sender = UserModel.objects.get(username=req.user.username)

    if message['receiver'] == str(sender.id):
        return Response({"error": "Cannot Send Messages To Yourself"}, status=status.HTTP_400_BAD_REQUEST)
    message['sender'] = sender.id
    serializer = SendMessageSerializer(data=message)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)




@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def messagesUnread(req):
    sender = UserModel.objects.get(username=req.user.username)
    messages = Message.objects.filter(Q(read=False) & Q(receiver=sender.id)).order_by('-sent_at')

    serializer = MessagesSerializer(messages, many=True)
    return Response(serializer.data)


