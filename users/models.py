import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

USER_NAME_MAX_LENGTH = 124
USER_SURNAME_MAX_LENGTH = 124
USER_PHONE_MAX_LENGTH = 12
USER_ABOUT_MAX_LENGTH = 256
AVATAR_UPLOAD_PATH = 'avatars/'

def generate_user_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.email.replace('@', '_').replace('.', '_')}.{ext}"
    return os.path.join(AVATAR_UPLOAD_PATH, filename)

class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        mail = self.normalize_email(email)
        user = self.model(
            email=mail,
            name=name,
            surname=surname,
            phone=phone,
            **extra_fields
        )
        user.avatar = 'avatars/temp.png' 
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, surname, phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
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
        blank=False, 
        null=False
    )
    
    phone = models.CharField(
        max_length=USER_PHONE_MAX_LENGTH, 
        verbose_name='Телефон'
    )
    
    github_url = models.URLField(
        blank=True, 
        null=True, 
        verbose_name='Ссылка на GitHub'
    )
    
    about = models.TextField(
        max_length=USER_ABOUT_MAX_LENGTH,
        blank=True, 
        null=True, 
        verbose_name='О себе'
    )
    
    is_active = models.BooleanField(
        default=True, 
        verbose_name='Активен'
    )
    
    is_staff = models.BooleanField(
        default=False, 
        verbose_name='Персонал'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phone']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.name} {self.surname} ({self.email})"