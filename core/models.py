import os

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models



def get_image_path(instance, filename):
    print(os.path.join('image_user', str(instance), filename))
    return os.path.join('image_user', str(instance), filename)

class CommonData(models.Model):

    device_ID = models.CharField(max_length=30,blank=True)

    latitude = models.FloatField(validators=[MinValueValidator(-90.00000000),
                                             MaxValueValidator(90.00000000)],null=True)

    longitude = models.FloatField(validators=[MinValueValidator(-180.00000000),
                                              MaxValueValidator(180.00000000)],null=True)

    name = models.CharField(max_length=30,blank=True)

    link_to_image = models.CharField(max_length=200)

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


