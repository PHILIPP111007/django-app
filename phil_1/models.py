from django.db import models

# Create your models here.


class Person(models.Model):
	name = models.CharField(max_length=20)
	surname = models.CharField(max_length=20)
	age = models.IntegerField()


class Admin(models.Model):
	login = models.CharField(max_length=20)
	password = models.CharField(max_length=30)