from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    context_dict = {}
    return render(request,'bandsnap/index.html',context=context_dict)

def signup(request):
    return HttpResponse("this will be the signup page")

def login(request):
    return HttpResponse("this will be the login page")

def search(request):
    return HttpResponse("this will be the search page")

def about(request):
    return HttpResponse("this will be the about page")