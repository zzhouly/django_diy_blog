from django.urls import path
from . import views

urlpatterns = [
	path('', views.HomeView.as_view(), name="home"),
	# path('blogger/<int:pk>', views.BlogListByUserView, name = "blogs-by-author"),
	# path('blogger/<int:pk>', views.BlogListByAuthorView.as_view(), name = "blogs-by-author"),
	path('<int:pk>/', views.BlogDetailView.as_view(), name="blog-detail"),
	# path('bolggers/', views.BloggerListView.as_view(), name="bloggers"),
	path('<int:pk>/comment/', views.BlogCommentCreate.as_view(), name="blog-comment"),
	path('create', views.BlogCreate, name="add-blog"),
	path('<int:pk>/update/', views.BlogUpdate.as_view(), name="update-blog"),
	path('<int:pk>/delete/', views.BlogDelete.as_view(), name="delete-blog"),
	path('category/<str:category>', views.BlogListByCategoryView, name = "blogs-by-category"),
	path('<int:pk>/like/', views.LikeView, name = "like_blog"),
	path('blog_following/', views.BlogListFollowingView, name="blog-following"),
	path('follower/', views.FollowerProfileListView.as_view(), name="follower"),
	path('following/', views.FollowingProfileListView.as_view(), name="following"),

	path('<int:pk>/image/', views.BlogImageCreate, name="blog_image"),
	path('image/<int:pk>/delete/', views.BlogImageDelete.as_view(), name="blog_image_delete"),
	path('image/<int:pk>', views.image_view, name = "image"),

]