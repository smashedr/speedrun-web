from django.db import models


class Results(models.Model):
    user = models.CharField(max_length=255)
    guess = models.IntegerField()
    offset = models.IntegerField()

    def __str__(self):
        return '{}: {} (-{})'.format(self.user, self.user, self.offset)


class Runs(models.Model):
    title = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    duration = models.IntegerField()
    no_guesses = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    results = models.ManyToManyField(Results)

    def __str__(self):
        return '{}: {}'.format(self.username, self.title)
