from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='users/change_password.html', success_url='/users/password_change/done/'), name='change_password'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
    
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('edit-profile/', views.ProfileEditView.as_view(), name='profile_edit'), 
    path('list/', views.UserListView.as_view(), name='user_list'),
    path('<int:pk>/', views.PublicProfileView.as_view(), name='public_profile'),
]