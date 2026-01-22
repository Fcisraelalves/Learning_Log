from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    text = models.CharField(max_length=30)
    date_added = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    def __str__(self):
        return self.text
    
class Entry(models.Model):
    text = models.TextField(max_length=100)
    date_added = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Entries'
    def __str__(self):
        return self.text
