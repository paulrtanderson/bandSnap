from django import template
from bandsnap.models import Artist, Band, Gig

register = template.Library()

@register.filter
def is_artist(user):
    try:
        artist = Artist.objects.get(user=user)
        return True
    except Artist.DoesNotExist:
        return False
    
@register.filter
def is_band(user):
    try:
        band = Band.objects.get(user=user)
        return True
    except Band.DoesNotExist:
        return False