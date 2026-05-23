from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import Http404

from .models import Project, Participation, Favorite
from .forms import ProjectForm

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12

    def get_queryset(self):
        return Project.objects.select_related('author').all()

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project-details.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_authenticated:
            context['is_favorite'] = Favorite.objects.filter(user=user, project=self.object).exists()
            context['is_participant'] = Participation.objects.filter(user=user, project=self.object).exists()
            context['is_author'] = (self.object.author == user)
        else:
            context['is_favorite'] = False
            context['is_participant'] = False
            context['is_author'] = False
            
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.pk})

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def test_func(self):
        project = self.get_object()
        return self.request.user == project.author

    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.pk})

class ProjectCompleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.status = 'COMPLETED'
        project.save()
        return redirect('projects:detail', pk=pk)

    def test_func(self):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return self.request.user == project.author

class JoinProjectView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if project.status == 'COMPLETED':
            raise Http404("Нельзя присоединиться к завершенному проекту")
        
        Participation.objects.get_or_create(user=request.user, project=project)
        return redirect('projects:detail', pk=pk)

class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        favorite, created = Favorite.objects.get_or_create(user=request.user, project=project)
        if not created:
            favorite.delete()
        return redirect('projects:detail', pk=pk)

class FavoriteListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'users/favorite_projects.html'
    context_object_name = 'favorites'
    paginate_by = 12

    def get_queryset(self):
        return Project.objects.filter(favorited_by__user=self.request.user).select_related('author')