import os
import django

# Manually configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wad_group_project_bandsnap.settings")
django.setup()

from bandsnap.models import Artist, Skill
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

if __name__ == '__main__':
    print("Populating database with artists...")
    populate()
    print("Population complete.")
