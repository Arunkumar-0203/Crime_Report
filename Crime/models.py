from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)

class PoliceStation(models.Model):
    station_name = models.CharField(max_length=50)

class UserReg(models.Model):
    login = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    contact = models.CharField(max_length=50,null=True)
    dob = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

class PoliceReg(models.Model):
    login = models.ForeignKey(User, on_delete=models.CASCADE)
    station = models.ForeignKey(PoliceStation, on_delete=models.CASCADE)
    contact = models.CharField(max_length=50)
    p_location = models.CharField(max_length=50)

class Criminals(models.Model):
    police = models.ForeignKey(PoliceReg, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/')
    contact = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    age = models.CharField(max_length=50)

class Feedback(models.Model):
    user = models.ForeignKey(UserReg, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=50)


class fir_reg(models.Model):

    timee = models.CharField(max_length=50)
    c_date = models.CharField(max_length=50)
    complaint = models.CharField(max_length=100)
    user = models.ForeignKey(UserReg, on_delete=models.CASCADE)
    police = models.ForeignKey(PoliceReg, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    charge = models.ImageField(upload_to='images/')