from django.db import models

# Create your models here.

class AdminSettings(models.Model):
    background_color = models.CharField(max_length=7, default='#FFFFFF')  # HEX-код
    font_color = models.CharField(max_length=7, default='#000000')
    font_size = models.PositiveIntegerField(default=14)

    def __str__(self):
        return "Admin Settings"
