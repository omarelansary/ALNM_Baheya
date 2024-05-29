from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class headDoctor(models.Model):
  email = models.EmailField(max_length = 255)
  password = models.CharField(max_length=500)
  firstName = models.CharField(max_length=250,default='Ahmed')
  lastName = models.CharField(max_length=250,default='Ezz')





  
  def __str__(self):
    return f"{self.email} is an admin."


