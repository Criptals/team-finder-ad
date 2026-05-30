import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

USER_NAME_MAX_LENGTH = 124
USER_SURNAME_MAX_LENGTH = 124
USER_PHONE_MAX_LENGTH = 12
USER_ABOUT_MAX_LENGTH = 256
AVATAR_UPLOAD_PATH = 'avatars/'


def generate_user_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.email.replace('@', '_').replace('.', '_')}.{ext}"
    return os.path.join(AVATAR_UPLOAD_PATH, filename)


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True,
        verbose_name='Email адрес'
    )
    name = models.CharField(
        max_length=USER_NAME_MAX_LENGTH,
        verbose_name='Имя'
    )
    surname = models.CharField(
        max_length=USER_SURNAME_MAX_LENGTH,
        verbose_name='Фамилия'
    )
    avatar = models.ImageField(
        upload_to=AVATAR_UPLOAD_PATH,
        verbose_name='Аватар',
        blank=True,
        default='avatars/temp.png'
    )
    phone = models.CharField(
        max_length=USER_PHONE_MAX_LENGTH,
        verbose_name='Телефон'
    )
    github_url = models.URLField(
        blank=True,
        default='',
        verbose_name='Ссылка на GitHub'
    )
    about = models.TextField(
        max_length=USER_ABOUT_MAX_LENGTH,
        blank=True,
        default='',
        verbose_name='О себе'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phone']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.name} {self.surname} ({self.email})'
