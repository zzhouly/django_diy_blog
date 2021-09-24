from django.db import models

# Create your models here.
from datetime import date
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django_resized import ResizedImageField


class Category(models.Model):
	name = models.CharField(max_length=200)

	def get_absolute_url(self):
		return reverse('home')

	def __str__(self):
		return self.name

class Profile(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	bio = models.TextField()
	profile_image = models.ImageField(null=True, blank=True, upload_to="images/profile")
	website_url = models.CharField(max_length=200, null=True, blank=True)
	facebook_url = models.CharField(max_length=200, null=True, blank=True)
	twitter_url = models.CharField(max_length=200, null=True, blank=True)
	insgram_url = models.CharField(max_length=200, null=True, blank=True)
	github_url = models.CharField(max_length=200, null=True, blank=True)
	follower = models.ManyToManyField(User, related_name="follower")
	following = models.ManyToManyField(User, related_name="following")


	def total_follower(self):
		return self.follower.count()


	def __str__(self):
		return str(self.user)


class Blog(models.Model):

	name = models.CharField(max_length=200)
	author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	description = RichTextField(blank=True, null=True)
	# header_image = ResizedImageField(size=[640, 480], null=True, blank=True, upload_to="images/")
	# header_image = models.ImageField(null=True, blank=True, upload_to="images/")
	# models.TextField(max_length=2000, help_text="Enter your blog text here.")
	post_date = models.DateTimeField(auto_now_add=True)
	category = models.CharField(max_length=200, default="coding")
	likes = models.ManyToManyField(User, related_name="blog_posts")

	class Meta:
		ordering = ["-post_date"]

	def total_likes(self):
		return self.likes.count()


	def get_absolute_url(self):
		return reverse('blog-detail', args=[str(self.id)])

	def __str__(self):
		return self.name 

class Image(models.Model):
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
	image = models.ImageField(null=True, blank=True, upload_to="images/")


class BlogComment(models.Model):
	description = RichTextField(blank=True, null=True)
	author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	post_date = models.DateTimeField(auto_now_add=True)
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

	class Meta:
		ordering = ["post_date"]

	def __str__(self):
		len_title=75
		if len(self.description)>len_title:
			titlestring=self.description[:len_title] + '...'
		else:
			titlestring=self.description
		return titlestring







