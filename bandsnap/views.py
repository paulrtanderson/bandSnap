from django.shortcuts import render
from django.http import HttpResponse
from bandsnap.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime

def index(request):
    context_dict = {}
    request.session.set_test_cookie()
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request,'bandsnap/index.html',context=context_dict)
    return response

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
    request.session.set_test_cookie()
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request,'bandsnap/about.html',context=context_dict)
    return response

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val
def visitor_cookie_handler(request):
    visits = int(request.COOKIES.get('visits', '1'))
    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('bandsnap:index'))


