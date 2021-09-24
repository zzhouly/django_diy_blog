from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.forms import modelformset_factory
from .models import Blog, BlogComment, Category, Profile, Image
from django.contrib.auth.models import User
from .forms import PostForm, EditForm, ImageForm, BlogCommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from itertools import chain
from django.contrib.auth.decorators import login_required, permission_required

class HomeView(generic.ListView):

    model = Blog 
    template_name = 'blog/home.html'
    ordering = ['-post_date']
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        cate_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['cate_menu'] = cate_menu

        return context 

def BlogListFollowingView(request):
    my_profile = Profile.objects.get(user=request.user)
    user = [user for user in my_profile.following.all()]
    posts = []
    qs=None

    for u in user:
        u_post = u.blog_set.all()
        posts.append(u_post)

    my_posts = request.user.blog_set.all()
    posts.append(my_posts)

    if len(posts)>0:
        qs = sorted(chain(*posts), reverse=True, key=lambda obj: obj.post_date)

    return render(request, "blog/blog_following.html", {'posts':qs})


class FollowerProfileListView(generic.ListView):
    model = Profile
    template_name = "blog/follower_list.html"

    def get_queryset(self):
        my_profile = Profile.objects.get(user=self.request.user)
        
        return my_profile.follower.all()


class FollowingProfileListView(generic.ListView):
    model = Profile
    template_name = "blog/following_list.html"

    def get_queryset(self):
        my_profile = Profile.objects.get(user=self.request.user)
        
        return my_profile.following.all()


def BlogListByCategoryView(request, category):

    category_blog = Blog.objects.filter(category = category.replace("-", " "))

    return render(request, 'blog/blog_list_by_category.html', {'category': category.title().replace("-", " "), 'category_blog': category_blog})


def LikeView(request, pk):
    print("LikeView")
    blog = get_object_or_404(Blog, id=request.POST.get('blog_id'))
    liked = False

    if blog.likes.filter(id=request.user.id).exists():
        blog.likes.remove(request.user)
        liked = False
    else:
        blog.likes.add(request.user)
        liked = True

    return HttpResponse(blog.total_likes())




class BlogDetailView(generic.DetailView):
    model = Blog 

    def get_context_data(self, *args, **kwargs):
        cate_menu = Category.objects.all()

        stuff = get_object_or_404(Blog, id = self.kwargs['pk'])
        total_likes = stuff.total_likes()
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context = super(BlogDetailView, self).get_context_data(*args, **kwargs)
        context['cate_menu'] = cate_menu
        context['total_likes'] = total_likes
        context['liked'] = liked


        return context



# class BlogCreate(LoginRequiredMixin, CreateView):
#   model = Blog
#   template_name = "blog/add_blog.html"
#   form_class = PostForm

@login_required
def BlogCreate(request):
 
    #'extra' means the number of photos that you can upload   ^
    if request.method == 'POST':
    
        postForm = PostForm(request.POST)
        imageForm = ImageForm(request.POST, request.FILES)
        images = request.FILES.getlist('image') #field name in model

        if postForm.is_valid() and imageForm.is_valid():
            post_instance = postForm.save(commit=False)
            post_instance.author = request.user
            post_instance.save()
            for img in images:
                image_instance = Image(blog=post_instance, image=img)
                image_instance.save()

            return HttpResponseRedirect(reverse("blog-detail", kwargs={'pk': post_instance.pk}))

    else:
        postForm = PostForm()
        imageForm = ImageForm()

    return render(request, 'blog/add_blog.html',{'postForm': postForm, 'imageForm': imageForm})


class BlogUpdate(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = "blog/update_blog.html"
    form_class = EditForm

    def get_context_data(self, *args, **kwargs):
        context = super(BlogUpdate, self).get_context_data(**kwargs)
        context['blog'] = get_object_or_404(Blog, pk = self.kwargs['pk'])
        return context

class BlogDelete(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = "blog/delete_blog.html"
    success_url = reverse_lazy('home')  


def image_view(request, pk):

    context = {}
    image = get_object_or_404(Image, pk = pk)
    context['image'] = image

    return render(request, "blog/image.html", context)

def BlogImageCreate(request, pk):

    if request.method == 'POST':
        blog_instance = get_object_or_404(Blog, pk = pk)
    
        imageForm = ImageForm(request.POST, request.FILES)
        images = request.FILES.getlist('image') #field name in model

        if imageForm.is_valid():

            for img in images:
                image_instance = Image(blog=blog_instance, image=img)
                image_instance.save()

            return HttpResponseRedirect(reverse('update-blog', kwargs={'pk': pk,}))

    else:
        imageForm = ImageForm()

    return render(request, 'blog/image_create.html',{'form': imageForm})

# class BlogImageCreate(LoginRequiredMixin, CreateView):
#     model = Image
#     form_class = ImageForm
#     template_name = "blog/image_create.html"

#     def form_valid(self, form):
#         blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
#         form.instance.blog = blog

#         return super(BlogImageCreate, self).form_valid(form)

#     def get_success_url(self):
#         return reverse('update-blog', kwargs={'pk': self.kwargs['pk'],})

class BlogImageDelete(LoginRequiredMixin, DeleteView):
    model = Image
    template_name = "blog/image_delete.html"

    def get_success_url(self):
        image = get_object_or_404(Image, pk = self.kwargs['pk'])
        return reverse('update-blog', kwargs={'pk': image.blog.id})



class BlogCommentCreate(LoginRequiredMixin, CreateView):
    model = BlogComment
    form_class = BlogCommentForm

    def get_context_data(self, **kwargs):
        context = super(BlogCommentCreate, self).get_context_data(**kwargs)
        context['blog'] = get_object_or_404(Blog, pk = self.kwargs['pk'])
        return context 

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog = get_object_or_404(Blog, pk = self.kwargs['pk'])

        return super(BlogCommentCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk'],})
