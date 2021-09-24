from django import forms
from .models import Blog, Category, Image, BlogComment
from django.db.utils import OperationalError

try:
	choices = Category.objects.all().values_list('name', 'name')
	choices_list=[]

	for choice in choices:
		choices_list.append(choice)
except OperationalError:
    pass



class PostForm(forms.ModelForm):

	class Meta:
		model = Blog
		fields = ('name', 'author', 'category', 'description',)

		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control'}),
			'author': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id': 'user', 'type': 'hidden'}),
			'category': forms.Select(choices=choices_list, attrs={'class': 'form-control'}),
			'description':forms.Textarea(attrs={'class': 'form-control'}),
		}

class EditForm(forms.ModelForm):
	class Meta:
		model = Blog
		fields = ('name', 'category', 'description',)

		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control'}),
			'category': forms.Select(choices=choices_list, attrs={'class': 'form-control'}),
			'description':forms.Textarea(attrs={'class': 'form-control'}),
			# 'header_image': forms.ClearableFileInput(attrs={'multiple': True}),
		}

class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ('image',)

		widgets = {
			'image': forms.ClearableFileInput(attrs={'multiple': True}),
		}

class BlogCommentForm(forms.ModelForm):
	class Meta:
		model = BlogComment
		fields = ('description',)

		widgets = {
			'description':forms.Textarea(attrs={'class': 'form-control'}),
		}

