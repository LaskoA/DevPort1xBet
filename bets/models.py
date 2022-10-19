from django.db import models


class Scrapedgame(models.Model):
    home = models.CharField(max_length=63)
    away = models.CharField(max_length=63)
    currentScore = models.CharField(max_length=10)
    market = models.CharField(max_length=300)
