from django.conf import settings
from django.db import models

class Project(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        CLOSED = 'closed', 'Closed'

    name = models.CharField(
        max_length=200, 
        verbose_name='Название проекта'
    )
    
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='Описание'
    )
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='owned_projects',
        verbose_name='Владелец'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Дата создания'
    )
    
    github_url = models.URLField(
        blank=True, 
        null=True, 
        verbose_name='Ссылка на GitHub'
    )
    
    status = models.CharField(
        max_length=6, 
        choices=Status.choices,
        default=Status.OPEN,
        verbose_name='Статус'
    )
    
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='participated_projects',
        blank=True, 
        verbose_name='Участники'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='favorites'
    )
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='favorited_by'
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user.email} favorited {self.project.name}'
