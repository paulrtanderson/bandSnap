from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    context_dict = {}
    return render(request,'bandsnap/index.html',context=context_dict)

def signup(request):
    context_dict = {}
    return render(request,'bandsnap/signup.html',context=context_dict)

def login(request):
    context_dict = {}
    return render(request,'bandsnap/login.html',context=context_dict)

def search(request):
    context_dict = {}
    return render(request,'bandsnap/search.html',context=context_dict)

def about(request):
    context_dict = {}
    return render(request,'bandsnap/about.html',context=context_dict)