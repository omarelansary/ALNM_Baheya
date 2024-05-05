from django.db import models

# Create your models here.
class Admin(models.Model):
  email = models.EmailField(max_length = 255)
  password = models.CharField(max_length=500)
  isAdmin = models.BooleanField(default=True)



  
  def __str__(self):
    return f"{self.email} is an admin."


