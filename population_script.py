import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','wad_group_project_bandsnap.settings')

import django
django.setup()

from django.contrib.auth.models import User
from bandsnap.models import Artist, Skill

def populate():

    # Create artists
    artists_data = [
        {
            "username": "artist1",
            "password": "password1",
            "photo_path": "path/to/photo1.jpg",
            "description": "Description of artist1",
            "skills": []  # Artist1 has skills in Singing and Guitar
        },
        {
            "username": "artist2",
            "password": "password2",
            "photo_path": "path/to/photo2.jpg",
            "description": "Description of artist2",
            "skills": []  # Artist2 has skills in Drums and Bass
        },
        # Add more artists as needed
    ]

    for artist_data in artists_data:
        user, created = User.objects.get_or_create(username=artist_data["username"])
        if created:
            user.set_password(artist_data["password"])
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
