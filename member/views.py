from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.urls import reverse_lazy, reverse
from .forms import SignUpForm, EditProfileForm, ProfileCreateForm, ProfileUpdateForm
from blog.models import Profile, Blog
from django.http import HttpResponseRedirect, HttpResponse


class ProfilePageView(generic.DetailView):
	model = Profile
	template_name = "registration/profile.html"

	def get_context_data(self, *args, **kwargs):
		profile = get_object_or_404(Profile, id=self.kwargs['pk'])
		blog_list = Blog.objects.filter(author=profile.user)

		total_follower = profile.total_follower()

		followed = False
		if profile.follower.filter(id=self.request.user.id).exists():
			followed = True

		context = super(ProfilePageView, self).get_context_data(*args, **kwargs)
		context['profile'] = profile
		context['blog_list'] = blog_list
		context['total_follower'] = total_follower
		context['followed'] = followed
		return context

class UpdateProfilePageView(generic.UpdateView):
	model = Profile
	template_name = "registration/profile_update.html"
	form_class = ProfileUpdateForm
	# fields = ['bio', 'profile_image', 'website_url', 'facebook_url', 'twitter_url', 'insgram_url', 'github_url']

	def get_success_url(self):
		return reverse('profile_page', kwargs={'pk': self.kwargs['pk'],})

class CreateProfilePageView(generic.CreateView):
	model = Profile
	template_name = "registration/profile_create.html"
	form_class = ProfileCreateForm
	# fields = ['bio', 'profile_image', 'website_url', 'facebook_url', 'twitter_url', 'insgram_url', 'github_url']

	def form_valid(self, form):
		form.instance.user = self.request.user

		return super(CreateProfilePageView, self).form_valid(form)

	def get_success_url(self):
		return reverse('home')


def FollowView(request, pk):
	profile = get_object_or_404(Profile, id=request.POST.get('profile_id'))
	my_profile = Profile.objects.get(user=request.user)
	followed = False
	value = "follow +"

	if profile.follower.filter(id=request.user.id).exists():
		profile.follower.remove(request.user)
		my_profile.following.remove(profile.user)

		followed = False
		value = "follow +"
	else:
		profile.follower.add(request.user)
		my_profile.following.add(profile.user)
		followed = True
		value = "unfollow"

	return HttpResponse(profile.total_follower())


def register_view(request):
	context = {}

	if request.POST:
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return HttpResponseRedirect(reverse('home'))
		else:
			context['form'] = form

	else:
		form = SignUpForm()
		context['form'] = form
	return render(request, 'registration/register.html', context)





class UserEditView(generic.UpdateView):
	form_class = EditProfileForm
	template_name = "registration/setting.html"
	success_url = reverse_lazy('home')

	def get_object(self):
		return self.request.user

class PasswordsChangeView(PasswordChangeView):
	template_name = "registration/password_change.html"
	form_class = PasswordChangeForm
	success_url = reverse_lazy('password_success')


def password_success(request):
	return render(request, "registration/password_success.html", {})



