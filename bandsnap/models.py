from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Skill(models.Model):
    name = models.CharField(max_length=200, unique=True)


    def __str__(self):
        return self.name


class Gig(models.Model):
    name = models.CharField(max_length=200, unique=True)
    date = models.DateField()
    venue_address = models.CharField(max_length=200)
    description = models.TextField()


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
    photo = models.ImageField()
    description = models.TextField()


    def __str__(self):
        return self.user.username
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True)
    description = models.TextField(blank=True)
    skills = models.ManyToManyField('Skill', blank=True)


class Artist(AbstractUser):
    has_skills = models.ForeignKey(Skill, on_delete=models.CASCADE, blank=True, null=True )
    requests = models.ManyToManyField("Band", through="Request")


class Band(AbstractUser):
    artists = models.ForeignKey(Artist, on_delete=models.CASCADE)
    gigs = models.ForeignKey(Gig, on_delete=models.CASCADE)
    needs_skills = models.ForeignKey(Skill, on_delete=models.CASCADE)


class Request(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    accepted = models.BooleanField()



    def __str__(self):
        return f"{self.artist}<->{self.band}@{self.date}:accepted={self.accepted}"