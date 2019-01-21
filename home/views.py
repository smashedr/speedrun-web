import json
import logging
from pprint import pformat
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from home.models import Run, Result

logger = logging.getLogger('app')
config = settings.CONFIG


def home_view(request):
    # View: /
    return render(request, 'home.html')


def user_view(request, username):
    # View: /<str:user>/
    logger.info('username: {}'.format(username))
    user = User.objects.get(username=username)
    runs = Run.objects.filter(user=user)
    data = {'runs': runs, 'user': user}
    return render(request, 'user.html', {'data': data})


@csrf_exempt
@require_http_methods(['POST'])
def submit_run(request):
    # View: /submit/
    try:
        data = json.loads(request.body.decode())
        logger.info(pformat(data))

        user, created = User.objects.get_or_create(username=data['user'])
        run = Run(
            user=user,
            title=data['title'],
            duration=data['duration'],
            no_guesses=data['no_guesses'],
        )
        run.save()

        for guess in data['data']:
            user, created = User.objects.get_or_create(username=guess['user'])
            result = Result(
                user=user,
                guess=guess['guess'],
                offset=guess['offset'],
            )
            result.save()
            run.results.add(result)

        return HttpResponse()

    except Exception as error:
        logger.exception(error)
        return HttpResponse(status=400)
