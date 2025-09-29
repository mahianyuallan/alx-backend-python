from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "parent_message", "timestamp")
    search_fields = ("sender__username", "receiver__username", "content")


admin.site.register(Message, MessageAdmin)
