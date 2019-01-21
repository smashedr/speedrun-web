import json
from django.db import models


class ResultField(models.TextField):
    description = "A run result field"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 65535
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return json.loads(value)


class Runs(models.Model):
    title = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    duration = models.IntegerField()
    no_guesses = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    results = ResultField()

    def __str__(self):
        return '{}: {}'.format(self.username, self.title)
