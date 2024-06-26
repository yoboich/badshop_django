import uuid

from django.db import models

from django.contrib.auth.models import AbstractBaseUser, Permission, Group
from django.contrib.auth.models import PermissionsMixin

from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save

from badshop_django.logger import logger
from .managers import CustomUserManager

import random
import string
def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True, verbose_name='Email adress', blank=True, null=True)
    first_name = models.CharField(u"First Name", max_length=100, blank=True, null=True)
    last_name = models.CharField(u"Last Name", max_length=100, blank=True, null=True)
    patronymic = models.CharField(u"Patronymic", max_length=100, blank=True, null=True)
    user_profile_id = models.IntegerField(blank=True, verbose_name='ID User', null=True)
    phone = models.CharField(max_length=24, blank=True, null=True, verbose_name='Phone')
    photo = models.ImageField(upload_to='midia/users/%Y/%m/%d/', blank=True, null=True, default='../static/assets/img/default_avatar.png',
                              verbose_name='Avatar')
    is_active = models.BooleanField(default=True, verbose_name='Activate', blank=True, null=True)
    is_admin = models.BooleanField(default=False, verbose_name='Administrator', blank=True, null=True)
    is_staff = models.BooleanField(_('staff status'), default=False, blank=True, null=True)
    is_superuser = models.BooleanField(_('super user'), default=False, blank=True, null=True)
    date_joined = models.DateTimeField(u'date joined', blank=True, null=True, default=timezone.now)
    last_login = models.DateTimeField(u'last login', blank=True, null=True)
    invited_by = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='invited_users')
    referral_code = models.CharField(max_length=6, unique=True, default=generate_referral_code, blank=True, null=True)
    bonus_points = models.FloatField(
        verbose_name='Бонусные баллы',
        default=0,
    )

    ADMINISTRATOR = 'AD'
    MANAGER = 'OA'
    CLIENT = 'CL'
    CLMANAGER = 'OO'

    TYPE_ROLE = [
        (ADMINISTRATOR, 'Administrator'),
        (MANAGER, 'Manager'),
        (CLIENT, 'Client'),
        (CLMANAGER, 'Client Manager')
    ]

    type = models.CharField(max_length=6, choices=TYPE_ROLE, default=CLIENT, verbose_name='Type User')
    ban = models.BooleanField(default=False, verbose_name='Baned')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @classmethod
    def create_account_for_unathourized_user(cls, email):
        try:
            user = cls.objects.get(email=email)
            created = False
            logger.debug(f'!account for user - {CustomUser.objects.get(email=email)}')
            logger.debug(f'!created - {created}')
            logger.debug(f'this email already in use - {user}')
        except:
            user = cls.objects.create_user(
                email=email, password=str(uuid.uuid4())
                )
            created = True
            logger.debug(f'user created - {user}')
        logger.debug(f'account for user - {user}')
        logger.debug(f'created - {created}')
        return user, created


    def __str__(self):
        return ' '.join(filter(None, (self.last_name, self.first_name, self.patronymic)))
        
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_absolute_url(self):
        return reverse('user_info', kwargs={'user_id': self.id})
    
    def save(self, *args, **kwargs):
        self.bonus_points = round(self.bonus_points, 2)
        super(CustomUser, self).save(*args, **kwargs)

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    metro = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    home_number = models.IntegerField(default=0, blank=True, null=True)
    room_number = models.IntegerField(default=0, blank=True, null=True)
    index = models.IntegerField(default=0, blank=True, null=True)
    info = models.CharField(max_length=255, blank=True, null=True)

    def full_address(self):
        full_address = ', '.join(filter(None, (
            self.region, 
            self.city, 
            self.street, 
            str(self.home_number), 
            str(self.room_number), 
            self.metro,
        )))
        return full_address

    def __str__(self):
        return self.user.__str__() + ' - ' + ','.join(filter(None, (self.city, self.street)))

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'





# ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ С ДОПОЛНИТЕЛЬНОЙ ИНФОРМАЦИЕЙ #
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def first_name(self):
        return self.user.first_name


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# Сигнал для выдачи бонусных баллов приглашивающему пользователю
@receiver(post_save, sender=CustomUser)
def give_referral_bonus(sender, instance, created, **kwargs):
    if created and instance.invited_by:  # Проверяем, что пользователь новый и был приглашен
        instance.invited_by.bonus_points += 0  # Предполагается, что пригласивший пользователь не получает бонусов
        instance.invited_by.save()
        instance.bonus_points += 300  # Выдаем бонусные баллы приглашенному пользователю
        instance.save()