# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ToDoList(models.Model):
    name = models.CharField(max_length=128)
    creation_date = models.DateField()
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

class ToDoItem(models.Model):
    description = models.TextField()
    completed = models.BooleanField(default=False)
    due_by = models.DateField()
    parent = models.ForeignKey(ToDoList)

    def __unicode__(self):
        return str(self.parent)+':'+self.description