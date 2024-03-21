from django.contrib.auth.models import User
from bandsnap.models import UserProfile, Request
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)

class RequestForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Request
        fields = ['message']