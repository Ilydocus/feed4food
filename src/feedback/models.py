from django.db import models

class Feedback(models.Model):
    TOPIC_CHOICES = [
        ('general', 'General Feedback'),
        ('bug', 'Bug Report'),
        ('feature', 'Feature Request'),
        ('usability', 'Usability Issue'),
        ('other', 'Other')
    ]
    
    topic = models.CharField(max_length=20, choices=TOPIC_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_topic_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"