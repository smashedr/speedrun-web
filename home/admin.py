from django.contrib import admin
from home.models import Run, Result

admin.site.register(Run)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_display = ('user', 'guess', 'offset')
