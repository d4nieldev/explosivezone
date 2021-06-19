from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from core.models import MenuOption, Exercise

def index(request):
    context = {
        'menu_data': str(MenuOption.get_root_options_html())
    }

    return render(request, 'index.html', context)

@csrf_exempt
def show_exercise(request):
    title = request.POST.get('exercise_title')
    ex = Exercise.objects.get(title=title)
    obj = {
        'title': ex.title,
        'youtube_link': ex.get_youtube_embed(),
        'exercise_list': ex.get_exercise_list(),
        'remarks': ex.remarks
    }

    return JsonResponse(obj)
