from ToDoApp.models import *
from django.core.management import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Clears Database"
    def  handle(self, *args, **options):
        ToDoItem.objects.all().delete()
        ToDoList.objects.all().delete()
