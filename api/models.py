from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")

    message = models.TextField()
    subject = models.CharField(max_length=150)

    read = models.BooleanField(default=False)
    sender_deleted = models.BooleanField(default=False)
    receiver_deleted = models.BooleanField(default=False)

    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.subject} | {self.message} | {self.pk} | {self.read}'
