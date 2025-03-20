from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('topic', 'created_at')
    list_filter = ('topic', 'created_at')
    search_fields = ('message',)
    readonly_fields = ('created_at',)