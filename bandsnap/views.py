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
from bandsnap.models import Artist, Band, Gig, Request
from bandsnap.forms import UserForm, RequestForm,ArtistForm,BandForm
from django.contrib import messages

def index(request):
    context_dict = {}
    context_dict['active_link'] = "index"
    response = render(request,'bandsnap/index.html',context=context_dict)
    return response

def signup(request):
    context_dict = {}
    registered = False

    user_form = UserForm()
    artist_form = ArtistForm()
    band_form = BandForm()
    
    context_dict['user_form'] = user_form
    context_dict['artist_form'] = artist_form
    context_dict['band_form'] = band_form
    context_dict['registered'] = registered
    context_dict['active_link'] = "signup"
    
    return render(request, 'bandsnap/signup.html', context_dict)

def signupartist(request):
    context_dict = {}
    registered = False
    
    if request.method == 'POST':

        user_form = UserForm(request.POST)
        artist_form = ArtistForm(request.POST)
        band_form = BandForm()

        
        if user_form.is_valid() and artist_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = artist_form.save(commit=False)
            profile.user = user
            
            if 'photo' in request.FILES:
                profile.photo = request.FILES['photo']
                
            profile.save()
            registered = True
        else:
            print(user_form.errors, artist_form.errors)
    else:
        user_form = UserForm()
        artist_form = ArtistForm()
    
    context_dict['user_form'] = user_form
    context_dict['artist_form'] = artist_form
    context_dict['band_form'] = band_form
    context_dict['registered'] = registered
    context_dict['active_link'] = "signup"
    
    return render(request, 'bandsnap/signup.html', context_dict)

def signupband(request):
    context_dict = {}
    registered = False
    
    if request.method == 'POST':

        user_form = UserForm(request.POST)
        band_form = BandForm(request.POST)
        artist_form = ArtistForm()

        
        if user_form.is_valid() and band_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = band_form.save(commit=False)
            profile.user = user
            
            if 'photo' in request.FILES:
                profile.photo = request.FILES['photo']
                
            profile.save()
            registered = True
        else:
            print(user_form.errors, band_form.errors)
    else:
        user_form = UserForm()
        band_form = ArtistForm()
    
    context_dict['user_form'] = user_form
    context_dict['artist_form'] = artist_form
    context_dict['band_form'] = band_form
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

def search_models(query):
    if query:
        artist_with_full_name = Artist.objects.annotate(full_name=Concat('user__first_name', Value(' '), 'user__last_name'))
        artists_by_name = artist_with_full_name.filter(full_name__icontains=query)
        artists_by_desc = Artist.objects.filter(description__icontains=query)
        artists_by_skills = Artist.objects.filter(skills__name__icontains=query)
        artists = (artists_by_name | artists_by_desc | artists_by_skills).distinct()
        
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

    return artists,bands,gigs
    
def display_search(request):
    query = request.GET.get('query')
    artists,bands,gigs = search_models(query)
        
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
            'band_username':profile.user.username,
            'user':request.user
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
            'address': escape(gig.venue_address),
            'date':gig.date
        })
        gigs_data.append(template)

    return_data = {"Artist":artists_data,
                   "Band":bands_data,
                   "Gig":gigs_data}
    return JsonResponse(return_data, safe=False)


def search(request):
    context_dict = {'active_link': 'search'}
    context_dict['form'] = RequestForm()
    return render(request,'bandsnap/search.html',context=context_dict)

def about(request):
    context_dict = {}
    context_dict['active_link'] = "about"
    response = render(request,'bandsnap/about.html',context=context_dict)
    return response
    
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('bandsnap:index'))

@login_required
def user_profile(request):
    context_dict = {'active_link': 'profile'}
    context_dict['user'] = request.user

    if is_artist(request.user):
            artist = Artist.objects.get(user = request.user)
            context_dict['userPhoto'] = artist.photo.url
            pending_requests = Request.objects.filter(artist=artist)
            context_dict['pending_requests'] = pending_requests
            if request.method == "POST":
                form = ArtistForm(request.POST, instance=artist)
                if form.is_valid():
                    profile = form.save(commit=False)
                    if 'photo' in request.FILES:
                        profile.photo = request.FILES['photo']
                    profile.save()
                    return redirect(reverse('bandsnap:user_profile'))
            else:
                form = ArtistForm(instance=artist)

            context_dict['form'] = form


    elif is_band(request.user):
            band = Band.objects.get(user=request.user)
            context_dict['userPhoto'] = band.photo.url
            context_dict['accepted_requests'] = Request.objects.filter(band=band,accepted=True)
            pending_requests = Request.objects.filter(band=band,accepted=False)
            context_dict['pending_requests'] = pending_requests
            if request.method == "POST":
                form = BandForm(request.POST, instance=band)
                if form.is_valid():
                    profile = form.save(commit=False)
                    if 'photo' in request.FILES:
                        profile.photo = request.FILES['photo']
                    profile.save()
                    return redirect(reverse('bandsnap:user_profile'))
            else:
                form = BandForm(instance=band)

            context_dict['form'] = form

    return render(request, 'bandsnap/user_profile.html', context=context_dict)

def accept_request(request):
    if request.method == "POST":
        join_request = Request.objects.get(id=request.POST.get('accept'))
        join_request.accepted = True
        join_request.save()
    return redirect(reverse('bandsnap:user_profile'))

def reject_request(request):
    if request.method == "POST":
        join_request = Request.objects.get(id=request.POST.get('reject'))
        join_request.delete()
    return redirect(reverse('bandsnap:user_profile'))

def is_artist(user):
    try:
        artist = Artist.objects.get(user=user)
        return True
    except Artist.DoesNotExist:
        return False
    

def is_band(user):
    try:
        band = Band.objects.get(user=user)
        return True
    except Band.DoesNotExist:
        return False



