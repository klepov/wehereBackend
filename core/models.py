from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
#
from rest_framework.authtoken.models import Token


class CommonData(models.Model):

    IMEI = models.IntegerField(null=True)
    device_ID = models.CharField(max_length=30,blank=True)

    latitude = models.FloatField(validators=[MinValueValidator(-90.00000000),
                                             MaxValueValidator(90.00000000)],null=True)

    longitude = models.FloatField(validators=[MinValueValidator(-180.00000000),
                                              MaxValueValidator(180.00000000)],null=True)

    class Meta:
        abstract = True

class Children(CommonData):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return str(self.user)

    def __str__(self):
        return str(self.user)


class Parent(CommonData):
    user = models.OneToOneField(User)
    child = models.ManyToManyField(Children,blank=True)


    def __unicode__(self):
        return str(self.user)

    def __str__(self):
        return str(self.user)


