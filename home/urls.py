from django.urls import path

import home.views as home

app_name = 'home'

urlpatterns = [
    path('', home.home_view, name='index'),
    path('submit/', home.submit_run, name='submit'),
    path('<str:username>/', home.user_view, name='user'),
]
