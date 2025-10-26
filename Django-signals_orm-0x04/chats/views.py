# chats/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from messaging.models import Message

@cache_page(60)  # cache this view for 60 seconds
def conversation_messages(request, username):
    """Retrieve all messages between the logged-in user and another user."""
    other_user = get_object_or_404(User, username=username)
    user = request.user

    # Retrieve messages between the logged-in user and the other user
    messages = (
        Message.objects.filter(sender=user, receiver=other_user) |
        Message.objects.filter(sender=other_user, receiver=user)
    ).order_by("timestamp")

    return render(request, "chats/conversation.html", {"messages": messages, "other_user": other_user})
