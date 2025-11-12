from django.db import models
from django.contrib.auth.models import User

class EthicsConsent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ethics_consent')
    has_given_consent = models.BooleanField(default=False)
    consent_given_at = models.DateTimeField(null=True, blank=True)
        
    def __str__(self):
        return f"{self.user.username} - {'Consent' if self.has_given_consent else 'No Consent'}"