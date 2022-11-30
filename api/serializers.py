from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Message
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class MessagesSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()

    def get_sender(self, obj):
        return obj.sender.username

    def get_receiver(self, obj):
        return obj.receiver.username

    class Meta:
        model = Message
        fields = ("id", "message", "subject", "sent_at", "sender", "receiver")


class SendMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("sender", "receiver", "message", "subject",)

