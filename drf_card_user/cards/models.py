from django.contrib.auth.models import User
from django.db import models


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_required = models.BooleanField(default=False)
    date = models.DateField()
    content = models.CharField(max_length=100, default="")
