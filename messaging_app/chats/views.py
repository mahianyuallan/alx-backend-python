from rest_framework import viewsets, permissions, mixins
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter, ConversationFilter
from rest_framework.decorators import action
from rest_framework.response import Response

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    filterset_class = ConversationFilter

    def get_queryset(self):
        # return only conversations that include the requesting user
        user = self.request.user
        return Conversation.objects.filter(participants=user).distinct()

    def perform_create(self, serializer):
        # Ensure the requesting user becomes a participant if not included
        conv = serializer.save()
        if self.request.user not in conv.participants.all():
            conv.participants.add(self.request.user)
            conv.save()

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related("conversation", "sender").all().order_by("-created_at")
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filterset_class = MessageFilter

    def get_queryset(self):
        qs = super().get_queryset()
        # If conversation id provided as query param, filter by it
        conv_id = self.request.query_params.get("conversation")
        if conv_id:
            qs = qs.filter(conversation__id=conv_id)
        # restrict messages to conversations where user is a participant
        user = self.request.user
        return qs.filter(conversation__participants=user).distinct().order_by("-created_at")

    def perform_create(self, serializer):
        # Ensure sender is the requesting user
        serializer.save(sender=self.request.user)
