import django_filters
from .models import Message, Conversation
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    # Filter messages by conversation id
    conversation = django_filters.NumberFilter(field_name="conversation__id")

    # Filter messages sent by a specific user id
    sender = django_filters.ModelChoiceFilter(field_name="sender", queryset=User.objects.all())

    # Time range on created_at
    created_at__gte = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_at__lte = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'created_at__gte', 'created_at__lte']

class ConversationFilter(django_filters.FilterSet):
    participant = django_filters.ModelChoiceFilter(field_name="participants", queryset=User.objects.all())

    class Meta:
        model = Conversation
        fields = ['participant']
