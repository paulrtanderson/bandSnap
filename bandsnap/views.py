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
from bandsnap.models import Artist, Band, Gig, Request, UserProfile
from bandsnap.forms import UserForm, UserProfileForm, RequestForm, SearchForm, NewSkillsForm
from django.contrib import messages

def index(request):
    context_dict = {}
    request.session.set_test_cookie()
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    context_dict['active_link'] = "index"

    if request.method == 'POST':
        search_form = SearchForm(request.POST)
    else:
        search_form = SearchForm()

    context_dict['search'] = search_form

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
    message = ""
    if (request.method == "POST"):
        print("recieved")
        form = RequestForm(request.POST)
        if (form.is_valid):
            band_username = request.POST.get('band_username')
            band = Band.objects.get(user__username=band_username)
            join_request = form.save(commit=False)
            join_request.artist = request.user.artist
            join_request.band = band
            join_request.save()
            return redirect(reverse("bandsnap:search"))
        else:
            print("form not valid")
            # Collecting all form errors
            form_errors = form.errors.get_json_data()
            for field, errors in form_errors.items():
                for error in errors:
                    print(error)
                    message += f"Error in {field}: {error['message']}" + "\n"
    
    return HttpResponse(message)
    
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
        accepted_artists = band.artists.filter(request__accepted=True)
        artist_names = [escape(artist.user.get_full_name()) for artist in accepted_artists]
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
    context_dict['artists'] = UserProfile.objects.filter(skills__name__icontains=request)
    context_dict['bands'] = Band.objects.filter(needs_skills__icontains=request)

    # Not sure what else to search by
    context_dict['gigs'] = Gig.objects.filter(name=request)

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
    # Add a request.method == POST to update profile picture/description


    context_dict = {'active_link': 'profile'}

    if request.user.artist.exist():
        context_dict['userType'] = 'band'
        # Artist is a type of user so hopefully this works?
        context_dict['userDetails'] = Band.objects.filter(artists__icontains=request.user)
        context_dict['gigDetails'] = Gig.objects.filter(band = request.user.band)
        #context_dict['userRequests'] = BandRequests.objects.filter(artists__icontains=request.user)

    elif request.user.skills.exist():
        context_dict['userType'] = 'artist'
        context_dict['userDetails'] = Artist.objects.filter(artist__user = request.user)        
        context_dict['userRequests'] = Request.objects.filter(artist__user = request.user)

    return render(request, 'bandsnap/user_profile.html', context=context_dict)

@login_required
def new_skills(request):
    context_dict = {}
    context_dict['active_link'] = "index"

    if request.method == 'POST':
        new_skills_form = NewSkillsForm(request.POST)
    else:
        new_skills_form = NewSkillsForm()

    context_dict['skills'] = new_skills_form()

    return render(request,'bandsnap/index.html',context=context_dict)




