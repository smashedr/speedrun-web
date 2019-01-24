import json
import logging
from pprint import pformat
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from home.models import Run, Result

logger = logging.getLogger('app')
config = settings.CONFIG


def home_view(request):
    #  View: /
    runs = Run.objects.all()
    runners = []
    for run in runs:
        if run.user not in runners:
            runners.append(run.user)
    data = {'runners': runners}
    return render(request, 'home.html', {'data': data})


def runner_view(request, username):
    #  View: /<str:username>/
    try:
        logger.debug('username: {}'.format(username))
        user = User.objects.get(username=username)
        runs = Run.objects.get_runs(user)
        data = {'runs': runs, 'user': user}
        return render(request, 'runner.html', {'data': data})
    except Exception as error:
        logger.exception(error)
        return redirect('home:index')


def run_view(request, username, run_pk):
    #  View: /<str:username>/<int:run_pk>/
    try:
        logger.debug('username: {}'.format(username))
        logger.debug('run_pk: {}'.format(run_pk))
        user = User.objects.get(username=username)
        run = Run.objects.get(pk=run_pk)
        results = Result.objects.filter(run=run)
        data = {'run': run, 'results': results, 'user': user}
        return render(request, 'run.html', {'data': data})
    except Exception as error:
        logger.exception(error)
        return redirect('home:index')


def user_results(request, username, runner=None):
    #  View: /results/<str:username>/
    try:
        logger.debug('username: {}'.format(username))
        user = User.objects.get(username=username)
        if runner:
            runner_user = User.objects.get(username=runner)
            results = Result.objects.filter(user=user, run__user=runner_user).order_by('-pk')
        else:
            results = Result.objects.filter(user=user).order_by('-pk')
        data = {'results': results, 'user': user, 'runner': runner}
        return render(request, 'user.html', {'data': data})
    except Exception as error:
        logger.exception(error)
        return redirect('home:index')


@csrf_exempt
@require_http_methods(['POST'])
def submit_run(request):
    #  View: /submit/
    try:
        data = json.loads(request.body.decode())
        logger.debug(pformat(data))
        user, created = User.objects.get_or_create(username=data['user'])
        run = Run(
            user=user,
            title=data['title'],
            duration=data['duration'],
            closest_offset=data['closest_offset'],
            no_guesses=data['no_guesses'],
        )
        run.save()

        for guess in data['data']:
            user, created = User.objects.get_or_create(username=guess['user'])
            result = Result(
                user=user,
                guess=guess['guess'],
                offset=guess['offset'],
                run=run,
            )
            result.save()

        data = {'url': run.get_url()}
        return JsonResponse(data)

    except Exception as error:
        logger.exception(error)
        data = {'error': error}
        return JsonResponse(data, status=400)
