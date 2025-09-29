from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification


class MessagingSignalTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="alicepass")
        self.user2 = User.objects.create_user(username="bob", password="bobpass")

    def test_notification_created_on_message(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hello Bob!"
        )
        # Check that notification exists
        notification = Notification.objects.filter(user=self.user2, message=message).first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, message)
