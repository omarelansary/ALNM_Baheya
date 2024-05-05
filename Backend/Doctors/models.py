from django.db import models

# Create your models here.
class Doctor(models.Model):
  firstName = models.CharField(max_length=200)
  lastName = models.CharField(max_length=200)
  email = models.EmailField(max_length = 255)
  password = models.CharField(max_length=500)


  
  def __str__(self):
    return f"{self.firstName} {self.lastName}"
