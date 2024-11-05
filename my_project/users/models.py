from django.db import models
from django.contrib.auth.models import User

from articles.models import Article

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saved_articles = models.ManyToManyField(Article, related_name='saved_by')
    
    def __str__(self):
        return f"Profile of {self.user.username}"
