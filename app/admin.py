from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.utils.translation import gettext_lazy as _


from app.models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'room_name', 'content', 'created_at', 'deleted')
    search_fields = ('user__username', 'room_name', 'content')  # Add search functionality
    list_filter = ('room_name', 'deleted', 'created_at')  # Filter messages by room, deletion status, or date

# Register the model with the MessageAdmin class
admin.site.register(Message, MessageAdmin)

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_id', 'object_repr', 'action_time', 'change_message')
    list_filter = ('action_time', 'user', 'content_type')
    search_fields = ('user__username', 'object_repr', 'change_message')
    ordering = ('-action_time',)
    date_hierarchy = 'action_time'

    fieldsets = (
        (None, {
            'fields': ('user', 'content_type', 'object_id', 'object_repr', 'action_time', 'change_message'),
        }),
    )

# Register LogEntry model in the admin
admin.site.register(LogEntry, LogEntryAdmin)
