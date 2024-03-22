from django.contrib.auth.models import User
from bandsnap.models import UserProfile, Request, Search
from django import forms


class UserForm(forms.ModelForm):
    Confirm_Password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)
        # Don't want this to be directly accessed, only changed via chooseUserType() JS
        exclude = ('user_type',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture', 'description', 'skills',)

class RequestForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Request
        fields = ['message']

class SearchForm(forms.ModelForm):
    CHOICES = [
        ('artists', 'Artists'),
        ('bands', 'Bands'),
        ('gigs', 'Gigs'),
    ]
    choice = forms.CharField(label="I'm looking for...", widget=forms.RadioSelect(choices=CHOICES))
    class Meta:
        model = Search
        fields = ['name']

class NewSkillsForm(forms.ModelForm):
    skills = forms.CharField(label="Type in your new skills. Format:skill1,skill2,skill3....", required=True)