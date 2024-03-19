from django.contrib import admin
from bandsnap.models import Artist,Band,Gig,Skill
# Register your models here.

admin.site.register(Artist)
admin.site.register(Band)
admin.site.register(Gig)
admin.site.register(Skill)
