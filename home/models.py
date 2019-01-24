from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class RunManager(models.Manager):
    def get_runs(self, user, runner=None):
        if runner:
            return self.filter(user=user, run__user=runner).order_by('-pk')
        else:
            return self.filter(user=user).order_by('-pk')


class Run(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=255)
    duration = models.IntegerField()
    closest_offset = models.IntegerField()
    no_guesses = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = RunManager()

    def __str__(self):
        return '{}: {}'.format(self.user.username, self.title)

    def get_winners(self):
        return Result.objects.filter(run=self.pk, offset=0)

    def get_closest(self):
        return Result.objects.filter(run=self.pk, offset=self.closest_offset)

    def get_url(self):
        uri = reverse('home:run', kwargs={'username': self.user.username, 'run_pk': self.pk})
        return '{}{}'.format(settings.SITE_URL, uri)


class ResultManager(models.Manager):
    def get_wins(self, user, runner=None):
        if runner:
            runner_user = User.objects.get(username=runner)
            return self.filter(offset=0, user=user, run__user=runner_user)
        else:
            return self.filter(offset=0, user=user)


class Result(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    guess = models.IntegerField()
    offset = models.IntegerField()
    run = models.ForeignKey(Run, models.CASCADE, blank=True, null=True)
    objects = ResultManager()

    def __str__(self):
        offset = '+{}'.format(self.offset) if self.offset > 0 else self.offset
        return '{}: {} ({})'.format(self.user, self.user, offset)
