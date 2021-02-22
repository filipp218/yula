from django.db import models
from datetime import date
# Create your models here.

class Team(models.Model):
    name = models.CharField("Название команды" , max_length = 25, blank=False)
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField("Имя" , max_length = 25, blank=False)
    lastname = models.CharField("Фамилия" , max_length = 25, blank=False)
    date_of_born = models.DateField("Дата рождения", default = date.today, blank=False)
    photo = models.ImageField("Фотка игрока", blank=False)
    description = models.TextField("Описание",  max_length = 150, blank=False)
    team = models.ForeignKey(Team, verbose_name="Команда" , on_delete=models.CASCADE,  blank=False)
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name + self.lastname


class Comment(models.Model):
    text = models.TextField("Коммент",  max_length = 250, blank=False)
    date = models.DateTimeField("Дата коммента", auto_now_add = True)
    for_who = models.ForeignKey(Player, verbose_name="Игрок" , on_delete=models.CASCADE,  blank=False)

    def __str__(self):
        return self.text

class Visitor(models.Model):
    first_visit = models.DateTimeField(auto_now_add = True)


class VisitHistory(models.Model):
    visitor = models.ForeignKey(Visitor,on_delete=models.CASCADE,  blank=False)
    player = models.ForeignKey(Player,on_delete=models.CASCADE,  blank=False)
    visit_time = models.DateTimeField(auto_now_add = True)
