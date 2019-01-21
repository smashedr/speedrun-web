import json
import logging
from pprint import pformat
from django.conf import settings
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from home.models import Runs
# from home.models import Results

logger = logging.getLogger('app')
config = settings.CONFIG


def home_view(request):
    # View: /
    return render(request, 'home.html')


def speedruns_view(request):
    # View: /speedruns/
    return render(request, 'speedruns.html')


@csrf_exempt
@require_http_methods(['POST'])
def submit_run(request):
    # View: /speedruns/
    try:
        data = json.loads(request.body.decode())
        logger.info(data)

        run = Runs(
            title=data['title'],
            username=data['username'],
            duration=data['duration'],
            no_guesses=data['no_guesses'],
            results=json.dumps(data['data']),
        )
        run.save()
        return HttpResponse()

    except Exception as error:
        logger.exception(error)
        return HttpResponse(status=400)
