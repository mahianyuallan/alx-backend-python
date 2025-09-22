from rest_framework import permissions
from .models import Conversation, Message  # adjust import path if needed

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow access only to participants of the conversation.

    - Authenticated users only (global setting already enforces IsAuthenticated)
    - For conversation-level actions: only participants may access.
    - For message-level actions: only participants of the message's conversation may access.
    """

    def _get_conversation_from_view(self, request, view):
        # Try common patterns where conversation id is in URL kwargs:
        # - 'conversation_pk'
        # - 'conversation_id'
        # - 'pk' (for conversation view)
        # - For nested routers, might be 'conversation'
        kw = view.kwargs
        for key in ("conversation_pk", "conversation_id", "conversation", "pk"):
            cid = kw.get(key)
            if cid:
                try:
                    return Conversation.objects.get(pk=cid)
                except Conversation.DoesNotExist:
                    return None
        return None

    def has_permission(self, request, view):
        # Only allow authenticated users (global setting covers this but keep check)
        if not request.user or not request.user.is_authenticated:
            return False

        # If listing conversations, allow (users should be able to list their own conversations)
        # But if listing messages for a conversation, ensure user is a participant
        if getattr(view, "basename", "") == "conversation" or view.__class__.__name__.lower().startswith("conversation"):
            # actions that create conversation (POST) are allowed for authenticated users;
            # We'll ensure creation data includes the requesting user or allow creation.
            return True

        # If there's a conversation in URL, check participant membership
        conv = self._get_conversation_from_view(request, view)
        if conv:
            return request.user in conv.participants.all()

        # If this is a message viewset and view.detail True, we'll check object-level permission instead
        return True

    def has_object_permission(self, request, view, obj):
        # obj can be a Conversation or a Message
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        if isinstance(obj, Message):
            conv = obj.conversation
            return request.user in conv.participants.all()

        # default deny
        return False
