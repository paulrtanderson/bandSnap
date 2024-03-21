from datetime import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import escape
from django.db.models import Q, Value
from django.db.models.functions import Concat
from bandsnap.models import Artist, Band, Gig
from bandsnap.forms import UserForm, UserProfileForm, RequestForm

def index(request):
    context_dict = {}
    request.session.set_test_cookie()
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    context_dict['active_link'] = "index"
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
    context_dict['active_link'] = "signup"
    
    return render(request, 'bandsnap/signup.html', context_dict)
def user_login(request):
    context_dict = {}
    context_dict['active_link'] = "login"
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
        return render(request, 'bandsnap/login.html',context=context_dict)
    
def join_band(request):
    query = request.POST.get('query')
    if (query and request.method == "POST"):
        form = RequestForm(request.POST)
        if (form.is_valid):
            band_username = request.POST.get('band_username')
            band = Band.objects.get(user__username=band_username)
            join_request = form.save(commit=False)
            join_request.artist = request.user.artist
            join_request.band = band
            join_request.save()
            return redirect(reverse("bandsnap:search"))
    
def artist_search(request):
    query = request.GET.get('query')
    if query:
        artist_with_full_name = Artist.objects.annotate(full_name=Concat('user__first_name', Value(' '), 'user__last_name'))
        artists_by_name = artist_with_full_name.filter(full_name__icontains=query)
        artists_by_desc = Artist.objects.filter(description__icontains=query)
        artists_by_skills = Artist.objects.filter(skills__name__icontains=query)
        artists = artists_by_name | artists_by_desc | artists_by_skills
        
        bands = Band.objects.filter(Q(user__first_name__icontains=query) |
                                    Q(description__icontains=query) |
                                    Q(needs_skills__name__icontains=query)).distinct()
        gigs = Gig.objects.filter(  Q(name__icontains=query) |
                                    Q(description__icontains=query) |
                                    Q(band__user__first_name__icontains=query) |
                                    Q(band__artists__in=artists_by_name) |
                                    Q(venue_address__icontains=query)).distinct()
    else:
        artists = Artist.objects.all()
        bands = Band.objects.all()
        gigs = Gig.objects.all()
        
    artists_data = []
    for profile in artists:
        skills = [escape(skill) for skill in profile.skills.all()]
        template = render_to_string('bandsnap/artists-result.html', {
            'profile_photo': escape(profile.photo.url),
            'name': escape(profile.user.get_full_name()),
            'description': escape(profile.description),
            'skills': skills
        })
        artists_data.append(template)
    bands_data = []
    for profile in bands:
        skills = [escape(skill) for skill in profile.needs_skills.all()]
        template = render_to_string('bandsnap/band-result.html', {
            'profile_photo': escape(profile.photo.url),
            'name': escape(profile.user.first_name),
            'description': escape(profile.description),
            'skills': skills,
            'form': RequestForm(),
            'band_username':profile.user.username
        })
        bands_data.append(template)

    gigs_data = []
    for gig in gigs:
        band  = gig.band
        artist_names = [escape(artist.user.get_full_name()) for artist in band.artists.all()]
        print(len(artists))
        template = render_to_string('bandsnap/gigs-result.html', {
            'profile_photo': escape(gig.band.photo.url),
            'bandname': escape(band.user.first_name),
            'name': escape(gig.name),
            'description': escape(gig.description),
            'artists': artist_names,
            'address': escape(gig.venue_address)
        })
        gigs_data.append(template)

    return_data = {"Artist":artists_data,
                   "Band":bands_data,
                   "Gig":gigs_data}
    return JsonResponse(return_data, safe=False)


def search(request):
    context_dict = {'active_link': 'search'}
    return render(request,'bandsnap/search.html',context=context_dict)

def about(request):
    context_dict = {}
    request.session.set_test_cookie()
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    context_dict['active_link'] = "about"
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

@login_required
def user_profile(request):
    return render(request, 'bandsnap/user_profile.py')




