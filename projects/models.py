from django.conf import settings
from django.db import models

class Project(models.Model):
    STATUS_CHOICES = [
        ('SEARCH', 'Поиск участников'),
        ('IN_PROGRESS', 'В разработке'),
        ('COMPLETED', 'Завершен'),
    ]

    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SEARCH', verbose_name="Статус")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_projects',
        verbose_name="Автор"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.title

class Participation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='participations'
    )
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='participants'
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')
        verbose_name = 'Участие'
        verbose_name_plural = 'Участия'

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