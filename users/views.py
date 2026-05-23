from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
import uuid
from django.contrib.auth import get_user_model
from .models import CustomUser
from .forms import RegisterForm, ProfileEditForm
from .utils import generate_avatar
from projects.models import Project, Favorite

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        
        email_prefix = form.cleaned_data.get('email').split('@')[0]
        unique_username = f"{email_prefix[:50]}_{uuid.uuid4().hex[:8]}"
        user.username = unique_username
        
        file_name = f"avatars/avatar_{user.email.replace('@', '_').replace('.', '_')}.png"
        user.avatar = file_name
        
        user.save()
        
        try:
            generate_avatar(user.email, file_name)
        except Exception as e:
            print(f"Ошибка генерации аватара: {e}")

        return redirect(self.success_url)

User = get_user_model()

class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    context_object_name = 'users'
    paginate_by = 12

    def get_queryset(self):
        qs = User.objects.all().order_by('-date_joined')
        filter_type = self.request.GET.get('filter')
        
        if not self.request.user.is_authenticated:
            return qs

        user = self.request.user

        if filter_type == 'owners-of-favorite-projects':
            qs = User.objects.filter(
                created_projects__favorited_by__user=user
            ).distinct()
            
        elif filter_type == 'owners-of-participating-projects':
            qs = User.objects.filter(
                created_projects__participants__user=user
            ).distinct()
            
        elif filter_type == 'interested-in-my-projects':
            qs = User.objects.filter(
                favorites__project__author=user
            ).distinct()
            
        elif filter_type == 'participants-of-my-projects':
            qs = User.objects.filter(
                participations__project__author=user
            ).exclude(pk=user.pk).distinct()
            
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_filter'] = self.request.GET.get('filter')
        return context

class PublicProfileView(DetailView):
    model = CustomUser
    template_name = 'users/user-details.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_projects'] = self.object.created_projects.all()
        return context

class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/user-details.html'
    context_object_name = 'profile_user'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_projects'] = self.object.created_projects.all()
        context['is_owner'] = True
        return context

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileEditForm
    template_name = 'users/edit_profile.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile')

