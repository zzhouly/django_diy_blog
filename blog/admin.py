from django.contrib import admin

# Register your models here.
from .models import Blog, BlogComment, Category, Profile, Image

admin.site.register(BlogComment)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Image)

class BlogCommentsInline(admin.TabularInline):
    model = BlogComment
    max_num = 0 

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'post_date')
    inlines = [BlogCommentsInline]

    def get_changeform_initial_data(self, request):
        get_data = super(BlogAdmin, self).get_changeform_initial_data(request)
        get_data['author'] = request.user.pk

        return get_data

