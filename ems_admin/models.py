from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class AuditTrail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.activity_name + ' ' + str(self.created_at)
