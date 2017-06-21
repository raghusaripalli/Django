from rest_framework import serializers
from ToDoApp.models import *

class listSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoList
        fields = ('id','name','creation_date','user')

class itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoItem
        fields = ('id','description','completed','due_by','parent')
