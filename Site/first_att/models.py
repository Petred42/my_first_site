import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Student(models.Model):  # модель профиля
    name = models.CharField(max_length=30, verbose_name="ФИО", null=True, blank=True)
    phone = models.CharField(max_length=12, verbose_name="Контактный телефон",  null=True, blank=True)
    about = models.TextField(verbose_name="О себе", null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="photos/", verbose_name="Фото", null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Student'


class Articles(models.Model):  # модель статьи
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='articles/')
    about = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    school = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(default=timezone.now())

    #
    # def get_absolute_url(self):
    #     return reverse('articles', args=[str(self.id)])
    #
    # class Events(models.Model):
    #     name = models.CharField(max_length=50)
    #     place = models.CharField(max_length=50)
    #     date = models.DateField()
    #     article = models.TextField()
    #     user = models.ForeignKey(User, on_delete=models.CASCADE)