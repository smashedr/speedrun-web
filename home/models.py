from django.contrib.auth.models import User
from django.db import models


class Result(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    guess = models.IntegerField()
    offset = models.IntegerField()

    def __str__(self):
        return '{}: {} (-{})'.format(self.user, self.user, self.offset)


class Run(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=255)
    duration = models.IntegerField()
    no_guesses = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    results = models.ManyToManyField(Result, blank=True)

    def __str__(self):
        return '{}: {}'.format(self.user, self.title)
