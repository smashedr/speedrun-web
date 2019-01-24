from django.urls import path

import home.views as home

app_name = 'home'

urlpatterns = [
    path('', home.home_view, name='index'),
    path('submit/', home.submit_run, name='submit'),
    path('runs/<str:username>/', home.runner_view, name='runner'),
    path('runs/<str:username>/<int:run_pk>/', home.run_view, name='run'),
    path('results/<str:username>/', home.user_results, name='user'),
    path('results/<str:username>/<str:runner>', home.user_results, name='user_runner'),
]
