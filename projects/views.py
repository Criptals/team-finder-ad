from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import Http404

from .models import Project, Favorite
from .forms import ProjectForm

USERS_PER_PAGE=12

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = USERS_PER_PAGE

    def get_queryset(self):
        return Project.objects.select_related('owner').prefetch_related('participants').all()

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project-details.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.select_related('owner').prefetch_related('participants')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_authenticated:
            context['is_favorite'] = Favorite.objects.filter(user=user, project=self.object).exists()
            context['is_participant'] = user in self.object.participants.all()
            context['is_owner'] = (self.object.owner == user)
        else:
            context['is_favorite'] = False
            context['is_participant'] = False
            context['is_owner'] = False
            
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.pk})

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def test_func(self):
        project = self.get_object()
        return self.request.user == project.owner

    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.pk})

class JoinProjectView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project.objects.select_related('owner'), pk=pk)
        
        if project.status != Project.Status.OPEN:
            raise Http404('К этому проекту нельзя присоединиться')
        
        if request.user in project.participants.all():
            project.participants.remove(request.user)
        else:
            project.participants.add(request.user)
            
        return redirect('projects:detail', pk=pk)

class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        favorite, created = Favorite.objects.get_or_create(user=request.user, project=project)
        if not created:
            favorite.delete()
        return redirect('projects:detail', pk=pk)


class ProjectCompleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.status = 'closed'
        project.save()
        return redirect('projects:detail', pk=pk)

    def test_func(self):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return self.request.user == project.owner
    

class FavoriteListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/favorite_projects.html'
    context_object_name = 'favorites'
    paginate_by = USERS_PER_PAGE

    def get_queryset(self):
        return Project.objects.filter(
            favorited_by__user=self.request.user
        ).select_related('owner').prefetch_related('participants').order_by('-id')