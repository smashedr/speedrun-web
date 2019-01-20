import logging
from django.conf import settings
from django.shortcuts import render

logger = logging.getLogger('app')
config = settings.CONFIG


def home_view(request):
    # View: /
    return render(request, 'home.html')


def speedruns_view(request):
    # View: /speedruns/
    return render(request, 'speedruns.html')
