from django.shortcuts import render
from django.http import HttpResponse
from bandsnap.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index(request):
    context_dict = {}
    return render(request,'bandsnap/index.html',context=context_dict)

def signup(request):
    context_dict = {}
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    context_dict['user_form'] = user_form
    context_dict['profile_form'] = profile_form
    context_dict['registered'] = registered
    
    return render(request, 'bandsnap/signup.html', context_dict)
def user_login(request):
    #context_dict = {}
    #return render(request,'bandsnap/login.html',context=context_dict)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('bandsnap:index'))
            else:
                return HttpResponse("Your bandsnap account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'bandsnap/login.html')

def search(request):
    context_dict = {}
    return render(request,'bandsnap/search.html',context=context_dict)

def about(request):
    context_dict = {}
    return render(request,'bandsnap/about.html',context=context_dict)
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('bandsnap:index'))


