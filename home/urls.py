from django.urls import path

import home.views as home

app_name = 'home'

urlpatterns = [
    path('', home.home_view, name='index'),
    path('speedruns/', home.speedruns_view, name='speedruns'),
]
