from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_chat_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_chat_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    # self-referential field for threaded conversations
    parent_message = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )

    def __str__(self):
        return f"Message {self.id} from {self.sender} to {self.receiver}"

    def get_thread(self):
        """
        Recursively fetch all replies to this message (threaded conversation).
        """
        thread = []
        for reply in self.replies.all().select_related("sender", "receiver").prefetch_related("replies"):
            thread.append(reply)
            thread.extend(reply.get_thread())  # recursive call
        return thread

    class Meta:
        ordering = ["timestamp"]  # ensure messages appear oldest → newest
