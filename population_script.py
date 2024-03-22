import os
import django

# Manually configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wad_group_project_bandsnap.settings")
django.setup()

from bandsnap.models import Artist, Skill,Gig,Band,Request
# Now you can access Django settings
from django.conf import settings
from pathlib import Path

# Get the path to the media folder
media_path = Path(settings.MEDIA_ROOT)

from django.contrib.auth.models import User

def delete_existing_data():
    Gig.objects.all().delete()
    Artist.objects.all().delete()
    Band.objects.all().delete()
    Skill.objects.all().delete()



def populate():

    # Delete existing data
    delete_existing_data()
    # Create skills if not exists
    skills = ["Singing", "Guitar", "Drums", "Bass", "Keyboard"]
    for skill_name in skills:
        skill, created = Skill.objects.get_or_create(name=skill_name)

    #create bands
    bands_data = [
        {
            "username": "band1",
            "password": "password1",
            "first_name":"The backburners",
            "photo_path": str(Path("profile_images" ) / "backbench.jpeg"),
            "description": "Description of band x",
            "needs_skills": ["Singing", "Guitar"]
        },
        {
            "username": "band2",
            "password": "password1",
            "first_name":"The best",
            "photo_path": str(Path("profile_images" ) / "best.jpeg"),
            "description": "Description of band x",
            "needs_skills": ["Bass", "Guitar"]
        },
        {
            "username": "band3",
            "password": "password1",
            "first_name":"The lucky ones",
            "photo_path": str(Path("profile_images" ) / "lucky.jpeg"),
            "description": "Description of band x",
            "needs_skills": ["Singing", "Guitar"]
        },
        {
            "username": "band4",
            "password": "password1",
            "first_name":"The nine",
            "photo_path": str(Path("profile_images" ) / "band.png"),
            "description": "Description of band x",
            "needs_skills": ["Singing", "Guitar"]
        },
        {
            "username": "band5",
            "password": "password5",
            "first_name": "The Rebels",
            "photo_path": str(Path("profile_images") / "rebel.jpeg"),
            "description": "Description of band 5",
            "needs_skills": ["Singing", "Drums"]
        }
    ]

    # Create artists
    artists_data = [
        {
            "username": "artist1",
            "password": "password1",
            "first_name":"John",
            "last_name":"Doe",
            "photo_path": str(Path("profile_images" ) / "johndoe.jpeg"),
            "description": "Description of artist1",
            "skills": ["Singing", "Guitar"]  # Artist1 has skills in Singing and Guitar
        },
        {
            "username": "artist2",
            "password": "password2",
            "first_name":"Mary",
            "last_name":"Sue",
            "photo_path":str(Path("profile_images" ) / "marysue.jpeg"),
            "description": "Description of artist2",
            "skills": ["Drums", "Bass"]  # Artist2 has skills in Drums and Bass
        },
                {
            "username": "artist3",
            "password": "password2",
            "first_name":"Jane",
            "last_name":"Smith",
            "photo_path": str(Path("profile_images" ) / "janesmith.jpeg"),
            "description": "Description of artist2",
            "skills": ["Singing", "Bass"]  # Artist2 has skills in Drums and Bass
        },
                {
            "username": "artist4",
            "password": "password2",
            "first_name":"Albert",
            "last_name":"Denkin",
            "photo_path": str(Path("profile_images" ) / "albertdenkin.jpeg"),
            "description": "Description of artist2",
            "skills": ["Drums", "Guitar"]  # Artist2 has skills in Drums and Bass
        },
        {
            "username": "artist5",
            "password": "password5",
            "first_name": "Emily",
            "last_name": "Brown",
            "photo_path": str(Path("profile_images") / "emilybrown.jpeg"),
            "description": "Description of artist 5",
            "skills": ["Keyboard", "Bass"]
        }
        # Add more artists as needed
    ]
    # Create gigs
    gigs_data = [
        {
            "name": "Spring Jam",
            "date": "2024-04-01",
            "venue_address": "123 Main St, Cityville, State",
            "description": "Join us for an evening of lively music and entertainment at Spring Jam!",
            "band_username": "band1"
        },
        {
            "name": "Summer Fest",
            "date": "2024-04-05",
            "venue_address": "456 Oak Ave, Townsville, State",
            "description": "Celebrate the summer season with our Summer Fest extravaganza! Don't miss out on the fun!",
            "band_username": "band1"
        },
        {
            "name": "Rock Showcase",
            "date": "2024-04-02",
            "venue_address": "789 Elm St, Villageton, State",
            "description": "Get ready to rock out at our Rock Showcase event featuring top local bands!",
            "band_username": "band2"
        },
        {
            "name": "Autumn Groove",
            "date": "2024-04-06",
            "venue_address": "321 Pine St, Hamletville, State",
            "description": "Experience the chill vibes and autumn groove at our exclusive Autumn Groove concert!",
            "band_username": "band2"
        },
        {
            "name": "Winter Wonderland",
            "date": "2024-04-03",
            "venue_address": "567 Maple Ave, Riverside, State",
            "description": "Step into a Winter Wonderland with enchanting music and festive cheer!",
            "band_username": "band3"
        },
        {
            "name": "Holiday Jam",
            "date": "2024-04-07",
            "venue_address": "890 Birch St, Lakeside, State",
            "description": "Join us for a Holiday Jam filled with merry tunes and joyful celebrations!",
            "band_username": "band3"
        },
        {
            "name": "Electric Shock",
            "date": "2024-04-04",
            "venue_address": "234 Cedar Ave, Hillcrest, State",
            "description": "Prepare to be electrified by the high-voltage performances at Electric Shock!",
            "band_username": "band4"
        },
        {
            "name": "Funky Fusion",
            "date": "2024-04-08",
            "venue_address": "678 Walnut St, Mountaintop, State",
            "description": "Groove to the funky beats and soulful melodies at our Funky Fusion extravaganza!",
            "band_username": "band4"
        },
        {
            "name": "Jazz Rendezvous",
            "date": "2024-04-09",
            "venue_address": "345 Cedar Ave, Lakeshore, State",
            "description": "Immerse yourself in the smooth sounds of Jazz Rendezvous, a night to remember!",
            "band_username": "band5"
        },
        {
            "name": "Blues Boulevard",
            "date": "2024-04-10",
            "venue_address": "901 Pine St, Seaside, State",
            "description": "Take a stroll down Blues Boulevard and let the soulful blues captivate your senses!",
            "band_username": "band5"
        }
    ]

    artist_band_assignments = [
        ("artist1", "band1"),
        ("artist2", "band1"),
        ("artist3", "band2"),
        ("artist4", "band2"),
        ("artist5", "band3"),
    ]

    for artist_data in artists_data:
        add_artist(artist_data)

    for band_data in bands_data:
        add_band(band_data)

    for gig_data in gigs_data:
        add_gig(gig_data)

    for artist_username, band_username in artist_band_assignments:
        artist = Artist.objects.get(user__username=artist_username)
        band = Band.objects.get(user__username=band_username)
        create_request(artist, band)

def add_artist(artist_data):
        user, created = User.objects.get_or_create(username=artist_data["username"])
        if created:
            user.set_password(artist_data["password"])
            user.save()

        user.first_name = artist_data["first_name"]
        user.last_name = artist_data["last_name"]
        user.save()
        artist, created = Artist.objects.get_or_create(user=user)
        artist.description = artist_data["description"]
        artist.photo = artist_data["photo_path"]
        
        # Assign skills to the artist
        for skill_name in artist_data["skills"]:
            skill = Skill.objects.get(name=skill_name)
            artist.skills.add(skill)
        artist.save()


def add_band(band_data):
        user, created = User.objects.get_or_create(username=band_data["username"])
        if created:
            user.set_password(band_data["password"])
            user.save()

        user.first_name = band_data["first_name"]
        user.save()
        band, created = Band.objects.get_or_create(user=user)
        band.description = band_data["description"]
        band.photo = band_data["photo_path"]

        # Assign skills to the band
        for skill_name in band_data["needs_skills"]:
            skill = Skill.objects.get(name=skill_name)
            band.needs_skills.add(skill)
        band.save()

def create_request(artist, band):
    request, created = Request.objects.get_or_create(artist=artist, band=band, defaults={'accepted': True})
    return request

def add_gig(gig_data):
    band = Band.objects.get(user__username=gig_data["band_username"])
    gig = Gig.objects.create(
        name=gig_data["name"],
        date=gig_data["date"],
        venue_address=gig_data["venue_address"],
        description=gig_data["description"],
        band=band
    )

if __name__ == '__main__':
    print("Populating database with artists...")
    populate()
    print("Population complete.")
