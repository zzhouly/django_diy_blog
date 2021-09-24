from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('register/', views.register_view, name="register"),
	# path('register/', views.UserRegisterView.as_view(), name="register"),
	path('edit_profile/', views.UserEditView.as_view(), name="setting"),
	path('password/', views.PasswordsChangeView.as_view(), name="password_change"),
	path('password_success/', views.password_success, name="password_success"),
	path('<int:pk>/profile', views.ProfilePageView.as_view(), name="profile_page"),
	path('<int:pk>/update_profile/', views.UpdateProfilePageView.as_view(), name="update_profile"),
	path('create_profile/', views.CreateProfilePageView.as_view(), name="create_profile"),
	path('<int:pk>/follow/', views.FollowView, name="follow"),

	]