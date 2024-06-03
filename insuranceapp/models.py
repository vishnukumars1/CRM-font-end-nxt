from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your models here.

class agent(models.Model):
    aadaar_number = models.BigIntegerField()
    pan_number = models.CharField(max_length=200)
    dob = models.DateField()
    qualification = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.BigIntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    profile = models.ImageField(upload_to='image/',null=True)