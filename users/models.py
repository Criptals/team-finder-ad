from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    
    bio = models.TextField(blank=True, verbose_name='О себе')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True, verbose_name='Аватар')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    github = models.URLField(blank=True, verbose_name='GitHub профиль')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email