from django.db import models

# Create your models here.
class Match(models.Model):
    matchId = models.IntegerField()

    def __str__(self):
        return self.matchId