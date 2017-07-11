from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
import datetime
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib import auth
from ToDoApp.models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


# Create your views here.
from ToDoApp.serializers import listSerializer, itemSerializer


def logout(request):
    auth.logout(request)
    return redirect('/auth/login/')

def mergedview(request):
    obj = ToDoList.objects.all()
    d = {}
    for x in obj:
        d[x] = ToDoItem.objects.values('description').filter(parent=x)

    template = loader.get_template("index.html")
    context={'dict': d}
    return HttpResponse(template.render(context, request))


class TotalListView(LoginRequiredMixin, ListView):
    model = ToDoList
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

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


#####################
    # Rest API's :-)
####################

class List_All( generics.ListCreateAPIView):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = listSerializer

    def get_queryset(self, queryset=None):
        try:
            print self.request.user
            return ToDoList.objects.filter(user__username = self.request.user)
        except:
            return Http404

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(List_All, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print "in post"
        i = datetime.datetime.now()
        request.POST._mutable = True
        request.POST['creation_date']=str(i).split(' ')[0]
        request.POST['user'] = self.request.user.id
        return self.create(request, *args, **kwargs)

class List_Specific(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = listSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        try:
            return ToDoList.objects.filter(user__username = self.request.user).get(pk=self.kwargs['pk'])
        except:
            return Http404

    def put(self, request, *args, **kwargs):
        kwargs['partial']=True
        return self.update(request, *args, **kwargs)

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
        request.POST._mutable = True
        request.POST['parent'] = self.kwargs['list_id']
        return self.create(request, *args, **kwargs)


class List_Specific_Item_Specific(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = itemSerializer

    def get_object(self, queryset=None):
        try:
            return ToDoItem.objects.filter(parent__user__username = self.request.user).filter(parent__id=self.kwargs['list_id']).get(id=self.kwargs['item_id'])
        except:
            return Http404

    def put(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.POST['parent'] = self.kwargs['list_id']
        return self.update(request, *args, **kwargs)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/ToDoApp/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})