from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.auth import logout

from core.models import MenuOption, Exercise

def index(request):
    context = {
        'menu_data': str(MenuOption.get_root_options_html()),
        'is_admin': request.user.is_superuser
    }

    return render(request, 'index.html', context)

@csrf_exempt
def show_exercise(request):
    title = request.POST.get('exercise_title')
    ex = Exercise.objects.get(menu_option=MenuOption.objects.get(title=title))
    obj = {
        'title': ex.menu_option.title,
        'youtube_link': ex.get_youtube_embed(),
        'exercise_list': ex.get_exercise_list(),
        'remarks': ex.remarks
    }

    return JsonResponse(obj)

def logout_user(request):
    logout(request)

    return redirect('index')
