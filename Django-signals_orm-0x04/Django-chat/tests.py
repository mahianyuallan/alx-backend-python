from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message


class ThreadedConversationTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="alicepass")
        self.user2 = User.objects.create_user(username="bob", password="bobpass")

    def test_threaded_conversation(self):
        msg1 = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello Bob!")
        reply1 = Message.objects.create(sender=self.user2, receiver=self.user1, content="Hi Alice!", parent_message=msg1)
        reply2 = Message.objects.create(sender=self.user1, receiver=self.user2, content="How are you?", parent_message=reply1)

        thread = msg1.get_thread()
        contents = [m.content for m in thread]

        self.assertIn("Hi Alice!", contents)
        self.assertIn("How are you?", contents)
        self.assertEqual(len(thread), 2)
