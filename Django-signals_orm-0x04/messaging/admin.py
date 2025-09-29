from django.contrib import admin
from .models import Message, Notification, MessageHistory


class MessageHistoryInline(admin.TabularInline):
    model = MessageHistory
    extra = 0
    readonly_fields = ("old_content", "edited_at")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "edited", "timestamp")
    search_fields = ("sender__username", "receiver__username", "content")
    inlines = [MessageHistoryInline]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "message", "is_read", "created_at")
    list_filter = ("is_read",)


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "old_content", "edited_at")
