from ToDoApp.models import *
from django.core.management import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Adds Sample Data( 5 lists with 5 entires each) to Database"
    def  handle(self, *args, **options):

        u1 = User.objects.get(id=1)
        u2 = User.objects.get(id=2)

        ToDoList(name="list1", creation_date="2017-04-02", user=u1).save()
        ToDoList(name="list2", creation_date="2017-05-02", user=u2).save()
        ToDoList(name="list3", creation_date="2017-05-26", user=u1).save()
        ToDoList(name="list4", creation_date="2017-06-12", user=u1).save()
        ToDoList(name="list5", creation_date="2017-04-16", user=u2).save()

        # todolists
        tlist = ToDoList.objects.get(name='list1')
        ToDoItem(description="item1", due_by="2017-01-01", parent=tlist).save()
        ToDoItem(description="item2", due_by="2017-01-02", parent=tlist).save()
        ToDoItem(description="item3", due_by="2017-01-03", parent=tlist).save()
        ToDoItem(description="item4", due_by="2017-01-04", parent=tlist).save()
        ToDoItem(description="item5", due_by="2017-01-05", parent=tlist).save()

        tlist = ToDoList.objects.get(name='list2')
        ToDoItem(description="item6", due_by="2017-02-01", parent=tlist).save()
        ToDoItem(description="item7", due_by="2017-02-02", parent=tlist).save()
        ToDoItem(description="item8", due_by="2017-02-03", parent=tlist).save()
        ToDoItem(description="item9", due_by="2017-02-04", parent=tlist).save()
        ToDoItem(description="item10", due_by="2017-02-05", parent=tlist).save()

        tlist = ToDoList.objects.get(name='list3')
        ToDoItem(description="item11", due_by="2017-05-01", parent=tlist).save()
        ToDoItem(description="item12", due_by="2017-05-02", parent=tlist).save()
        ToDoItem(description="item13", due_by="2017-05-03", parent=tlist).save()
        ToDoItem(description="item14", due_by="2017-05-04", parent=tlist).save()
        ToDoItem(description="item15", due_by="2017-05-05", parent=tlist).save()

        tlist = ToDoList.objects.get(name='list4')
        ToDoItem(description="item16", due_by="2017-03-01", parent=tlist).save()
        ToDoItem(description="item17", due_by="2017-03-02", parent=tlist).save()
        ToDoItem(description="item18", due_by="2017-03-03", parent=tlist).save()
        ToDoItem(description="item19", due_by="2017-03-04", parent=tlist).save()
        ToDoItem(description="item20", due_by="2017-03-05", parent=tlist).save()

        tlist = ToDoList.objects.get(name='list5')
        ToDoItem(description="item21", due_by="2017-04-01", parent=tlist).save()
        ToDoItem(description="item22", due_by="2017-04-02", parent=tlist).save()
        ToDoItem(description="item23", due_by="2017-04-03", parent=tlist).save()
        ToDoItem(description="item24", due_by="2017-04-04", parent=tlist).save()
        ToDoItem(description="item25", due_by="2017-04-05", parent=tlist).save()