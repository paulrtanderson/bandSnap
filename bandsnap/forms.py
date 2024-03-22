from django.contrib.auth.models import User
from bandsnap.models import Request, AbstractUser,Artist,Band
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ('photo', 'description','skills')

class BandForm(forms.ModelForm):
    class Meta:
        model = Band
        fields = ('photo', 'description','needs_skills')

class RequestForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Request
        fields = ['message']

class NewSkillsForm(forms.ModelForm):
    skills = forms.CharField(label="Type in your new skills. Format:skill1,skill2,skill3....", required=True)