from django.db import models


class Organization(models.Model):
    title = models.CharField(max_length=255)


class Dataset(models.Model):
    title = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization)


class Project(models.Model):
    title = models.CharField(max_length=255)
