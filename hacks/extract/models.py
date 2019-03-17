from django.db import models
from django.urls import reverse
# Create your models here.

class Document(models.Model):
    document = models.FileField(upload_to='documents/')
    name = models.CharField(max_length=100,default="do")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def return_pk(self):
        return self.pk
    def get_absolute_url(self):
        return reverse('document',kwargs={'pk': self.pk})

class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=70)
    comment = models.TextField()
