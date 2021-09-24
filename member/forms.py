from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from blog.models import Profile

class SignUpForm(UserCreationForm):

	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class EditProfileForm(UserChangeForm):

	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password',)

class ProfileCreateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('bio', 'profile_image', 'website_url', 'facebook_url', 'twitter_url', 'insgram_url', 'github_url')

		widgets = {
			'bio': forms.Textarea(attrs={'class': 'form-control'}),
			'website_url': forms.TextInput(attrs={'class': 'form-control',}),
			'facebook_url': forms.TextInput(attrs={'class': 'form-control'}),
			'twitter_url':forms.TextInput(attrs={'class': 'form-control'}),
			'insgram_url':forms.TextInput(attrs={'class': 'form-control'}),
			'github_url':forms.TextInput(attrs={'class': 'form-control'}),
		}

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('bio', 'profile_image', 'website_url', 'facebook_url', 'twitter_url', 'insgram_url', 'github_url')

		widgets = {
			'bio': forms.Textarea(attrs={'class': 'form-control'}),
			'website_url': forms.TextInput(attrs={'class': 'form-control',}),
			'facebook_url': forms.TextInput(attrs={'class': 'form-control'}),
			'twitter_url':forms.TextInput(attrs={'class': 'form-control'}),
			'insgram_url':forms.TextInput(attrs={'class': 'form-control'}),
			'github_url':forms.TextInput(attrs={'class': 'form-control'}),
		}
