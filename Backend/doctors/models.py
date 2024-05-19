from django.db import models


    
# Create your models here.
class Doctor(models.Model):
  # patients = models.ManyToManyField('patients.Patient')
  assessments = models.ManyToManyField('assessments.Assessment')

  firstName = models.CharField(max_length=250)
  lastName = models.CharField(max_length=250)
  email = models.EmailField(max_length = 255)
  password = models.CharField(max_length=500)

  
  def __str__(self):
    return f"{self.firstName} {self.lastName}"


