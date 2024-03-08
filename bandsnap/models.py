from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Skill(models.Model):
    name = models.CharField(max_length=200, primary_key=True)


class Gig(models.Model):
    date = models.DateField()
    venue_address = models.CharField(max_length=200)
    description = models.TextField()


# Bands and Artists will be implemented through the Django User object.
# We can then create a new table to hold data about Artists and Bands 
# and create a 1:1 relationship between that and Users.

# Artist and Band inherit from this model
class AbstractUser(models.Model):


    class Meta:
        abstract = True


    username = models.OneToOneField(User,
                                    parent_link=User.username, 
                                    on_delete=models.PROTECT, 
                                    primary_key=True)
    photo = models.ImageField()
    description = models.TextField()


    def __str__(self):
        return self.username


class Band(AbstractUser):
    needs_skills = models.ForeignKey(Skill, on_delete=models.CASCADE)
    gigs = models.ForeignKey(Gig, on_delete=models.CASCADE)


class Artist(AbstractUser):
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    has_skills = models.ForeignKey(Skill, on_delete=models.CASCADE)


class Request(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    accepted = models.BooleanField()
    # TODO use this for extra fields on the many-many relationship between bands and artists
