import os
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Members(models.Model):
    name = models.ForeignKey(User)
    photo = models.FileField(upload_to='members/',blank=True, default='members/no-photo.png')
    goal_weight = models.CharField(max_length=5)
    initial_weight = models.CharField(max_length=5)

    class Meta:
        verbose_name = 'Member'
        verbose_name_plural = 'Members'

    def __str__(self):
        return '{} {}'.format(self.name.first_name,self.name.last_name)

class Weighins(models.Model):
    member = models.ForeignKey(Members,null=True,on_delete=models.PROTECT)
    date = models.DateField()
    weight = models.CharField(max_length=5)
    photo = models.FileField(upload_to='weighins/',blank=False)
    left_arm = models.CharField(max_length=5,verbose_name='Left Arm (inches)',blank=True)
    right_arm = models.CharField(max_length=5,verbose_name='Right Arm (inches)',blank=True)
    left_leg = models.CharField(max_length=5,verbose_name='Left Leg (inches)',blank=True)
    right_leg = models.CharField(max_length=5,verbose_name='Right Leg (inches)',blank=True)
    waist = models.CharField(max_length=5,verbose_name='Waist (inches)',blank=True)
    bum = models.CharField(max_length=5,verbose_name='Bum (inches)',blank=True)
    chest = models.CharField(max_length=5,verbose_name='Chest (inches)',blank=True)

class ProgressPhotos(models.Model):
    member = models.ForeignKey(Members,related_name='photos',null=True,on_delete=models.PROTECT) #set_null does not delete the equipment when deleting the photo
    photo = models.FileField(upload_to='member_progress',blank=False)
    date = models.DateField()

class Payments(models.Model):
    member = models.ForeignKey(Members,null=True,on_delete=models.PROTECT)
    amount = models.IntegerField()
    date = models.DateField()
