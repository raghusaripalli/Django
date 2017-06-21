from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework import generics

from ToDoApp.models import *


# Create your views here.
from ToDoApp.serializers import listSerializer, itemSerializer


def mergedview(request):
    obj = ToDoList.objects.all()
    d = {}
    for x in obj:
        d[x] = ToDoItem.objects.values('description').filter(parent=x)

    template = loader.get_template("index.html")
    context={'dict': d}
    return HttpResponse(template.render(context, request))


class TotalListView(ListView):
    model = ToDoList

    def get_context_data(self, **kwargs):
        context = super(TotalListView, self).get_context_data(**kwargs)
        context['ram'] = ToDoList.objects.all()
        return context


class ItemsDetailView(DetailView):
    model = ToDoList

    def get_context_data(self, **kwargs):
        print kwargs, 'jimpak', self.kwargs, 'chimpak'
        context = super(ItemsDetailView, self).get_context_data(**kwargs)
        print context
        context['ram'] = ToDoItem.objects.filter(parent_id=kwargs['object'])
        return context


class CreateTodoList(LoginRequiredMixin, CreateView):
    model = ToDoList
    fields = ['name', 'creation_date']
    success_url = reverse_lazy('homepage')
    pass


class UpdateTodoList(LoginRequiredMixin, UpdateView):
    model = ToDoList
    fields = ['name', 'creation_date']
    success_url = reverse_lazy('homepage')


class DeleteTodoList(LoginRequiredMixin, DeleteView):
    model = ToDoList
    field = ['name', 'creation_date']
    success_url = reverse_lazy('homepage')


#################
    # Rest API's :-)
#################

class List_All(generics.ListCreateAPIView):
    serializer_class = listSerializer

    def get_queryset(self, queryset=None):
        try:
            return ToDoList.objects.filter(user__username = self.request.user)
            pass
        except:
            return Http404


class List_Specific(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = listSerializer

    def get_object(self, queryset=None):
        try:
            return ToDoList.objects.filter(user__username = self.request.user).get(pk=self.kwargs['pk'])
        except:
            return Http404

class Item_All(generics.ListCreateAPIView):
    serializer_class = itemSerializer

    def get_queryset(self, queryset=None):
        try:
            return ToDoItem.objects.filter(parent__user__username = self.request.user)
        except:
            return Http404

class Item_Specific(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = itemSerializer

    def get_object(self, queryset=None):
        try:
            return ToDoItem.objects.filter(parent__user__username = self.request.user).get(pk=self.kwargs['pk'])
        except:
            return Http404

class List_Specific_Item(generics.ListCreateAPIView):
    serializer_class = itemSerializer

    def get_queryset(self, queryset=None):
        try:
            return ToDoItem.objects.filter(parent__user__username = self.request.user).filter(parent__id=self.kwargs['list_id'])
        except:
            return Http404

    def post(self, request, *args, **kwargs):
        request.data['parent'] = self.kwargs['list_id']
        return self.create(request, *args, **kwargs)


class List_Specific_Item_Specific(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = itemSerializer

    def get_object(self, queryset=None):
        try:
            return ToDoItem.objects.filter(parent__user__username = self.request.user).filter(parent__id=self.kwargs['list_id']).get(id=self.kwargs['item_id'])
        except:
            return Http404

    def put(self, request, *args, **kwargs):
        request.data['parent'] = self.kwargs['list_id']
        return self.update(request, *args, **kwargs)