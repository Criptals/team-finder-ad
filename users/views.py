import logging
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from .models import User
from .forms import RegisterForm, ProfileEditForm
from .utils import generate_avatar
USERS_PER_PAGE = 12

FILTER_OWNERS_FAVORITE = 'owners-of-favorite-projects'
FILTER_OWNERS_PARTICIPATING = 'owners-of-participating-projects'
FILTER_INTERESTED_IN_MINE = 'interested-in-my-projects'
FILTER_PARTICIPANTS_OF_MINE = 'participants-of-my-projects'

logger = logging.getLogger(__name__)

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        file_name = f"avatars/avatar_{user.email.replace('@', '_').replace('.', '_')}.png"
        user.avatar = file_name
        user.save()
        try:
            generate_avatar(user.email, file_name)
            logger.info(f"Аватар успешно сгенерирован для {user.email}")
        except Exception as e:
            logger.error(f"Ошибка генерации аватара для {user.email}: {e}")
        return redirect(self.success_url)

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'users/edit_profile.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile')

class PublicProfileView(DetailView):
    model = User
    template_name = 'users/user-details.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_projects'] = self.object.owned_projects.all()
        return context

class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    context_object_name = 'users'
    paginate_by = USERS_PER_PAGE

    def get_queryset(self):
        qs = User.objects.select_related()
        
        filter_type = self.request.GET.get('filter')
        
        if not self.request.user.is_authenticated:
            return qs

        user = self.request.user

        if filter_type == FILTER_OWNERS_FAVORITE:
            qs = User.objects.filter(
                owned_projects__favorited_by__user=user
            ).distinct()
            
        elif filter_type == FILTER_OWNERS_PARTICIPATING:
            qs = User.objects.filter(
                owned_projects__participants=user
            ).distinct()
            
        elif filter_type == FILTER_INTERESTED_IN_MINE:
            qs = User.objects.filter(
                favorites__project__owner=user
            ).distinct()
            
        elif filter_type == FILTER_PARTICIPANTS_OF_MINE:
            qs = User.objects.filter(
                participated_projects__owner=user
            ).exclude(pk=user.pk).distinct()
            
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_filter'] = self.request.GET.get('filter')
        return context


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user-details.html'
    context_object_name = 'profile_user'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_projects'] = self.object.owned_projects.all()
        return context