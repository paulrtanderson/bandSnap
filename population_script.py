import os
import django

# Manually configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wad_group_project_bandsnap.settings")
django.setup()

from bandsnap.models import Artist, Skill,Gig,Band
# Now you can access Django settings
from django.conf import settings
from pathlib import Path

# Get the path to the media folder
media_path = Path(settings.MEDIA_ROOT)

from django.contrib.auth.models import User

def delete_existing_data():
    Artist.objects.all().delete()
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
            "photo_path": str(Path("profile_images" ) / "image1.jpeg"),
            "description": "Description of band x",
            "needs_skills": ["Singing", "Guitar"]
        },
        {
            "username": "band2",
            "password": "password1",
            "first_name":"The best",
            "photo_path": str(Path("profile_images" ) / "image1.jpeg"),
            "description": "Description of band x",
            "needs_skills": ["Bass", "Guitar"]
        },
        {
            "username": "band3",
            "password": "password1",
            "first_name":"The lucky ones",
            "photo_path": str(Path("profile_images" ) / "image1.jpeg"),
            "description": "Description of band x",
            "needs_skills": ["Singing", "Guitar"]
        },
        {
            "username": "band4",
            "password": "password1",
            "first_name":"The nine",
            "photo_path": str(Path("profile_images" ) / "image1.jpeg"),
            "description": "Description of band x",
            "needs_skills": ["Singing", "Guitar"]
        },
    ]

    # Create artists
    artists_data = [
        {
            "username": "artist1",
            "password": "password1",
            "first_name":"John",
            "last_name":"Doe",
            "photo_path": str(Path("profile_images" ) / "image1.jpeg"),
            "description": "Description of artist1",
            "skills": ["Singing", "Guitar"]  # Artist1 has skills in Singing and Guitar
        },
        {
            "username": "artist2",
            "password": "password2",
            "first_name":"Mary",
            "last_name":"Sue",
            "photo_path":"image1.jpeg",
            "description": "Description of artist2",
            "skills": ["Drums", "Bass"]  # Artist2 has skills in Drums and Bass
        },
                {
            "username": "artist3",
            "password": "password2",
            "first_name":"Jane",
            "last_name":"Smith",
            "photo_path": "image1.jpeg",
            "description": "Description of artist2",
            "skills": ["Singing", "Bass"]  # Artist2 has skills in Drums and Bass
        },
                {
            "username": "artist4",
            "password": "password2",
            "first_name":"Albert",
            "last_name":"Denkin",
            "photo_path": "image1.jpeg",
            "description": "Description of artist2",
            "skills": ["Drums", "Guitar"]  # Artist2 has skills in Drums and Bass
        },
        # Add more artists as needed
    ]

    for artist_data in artists_data:
        add_artist(artist_data)

    for band_data in bands_data:
        add_band(band_data)

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
        

        # Assign skills to the artist
        for skill_name in band_data["needs_skills"]:
            skill = Skill.objects.get(name=skill_name)
            band.needs_skills.add(skill)

        band.save()


if __name__ == '__main__':
    print("Populating database with artists...")
    populate()
    print("Population complete.")
