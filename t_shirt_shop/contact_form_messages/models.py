from django.db import models

# Create your models here.


class MessagesModel(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=False)
    message = models.TextField(max_length=500)

    class Meta:
        verbose_name_plural = 'Contact messages'
