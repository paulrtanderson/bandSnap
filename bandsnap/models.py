from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


# Bands and Artists will be implemented through the Django User object.
# We can then create a new table to hold data about Artists and Bands 
# and create a 1:1 relationship between that and Users.

# Artist and Band inherit from this model
class AbstractUser(models.Model):
    class Meta:
        abstract = True

    user = models.OneToOneField(User,
                                on_delete=models.PROTECT, 
                                primary_key=True)
    user_type = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='profile_images', blank=True)
    description = models.TextField()

    def __str__(self):
        return self.user.username
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    description = models.TextField(blank=True)
    skills = models.ManyToManyField('Skill', blank=True)

    def __str__(self):
        return self.user.username


class Artist(AbstractUser):
    skills = models.ManyToManyField(Skill)


class Band(AbstractUser):
    # Band needs a name????
    artists = models.ManyToManyField(Artist, through='Request')
    needs_skills = models.ManyToManyField(Skill)


class Gig(models.Model):
    name = models.CharField(max_length=200, unique=True)
    date = models.DateField()
    venue_address = models.CharField(max_length=200)
    description = models.TextField()
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='gigs',default=None)


class Request(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    message = models.TextField(blank=True)

    class Meta:
        unique_together = ('artist', 'band')

    def __str__(self):
        return f"{self.artist}<->{self.band}@{self.date}:accepted={self.accepted}"
    
class Search(models.Model):
    name = models.CharField(max_length=200, unique=True,)
   