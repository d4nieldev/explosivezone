from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from core.forms import UserForm

from core.models import MenuOption, Exercise, Favorite


def BASE_CONTEXT(request):
    return dict({
        'menu_data': str(MenuOption.get_root_options_html(request.user.is_superuser, Favorite.objects.filter(user=request.user))),
        'is_admin': request.user.is_superuser,
        'debug': settings.DEBUG,
    })

def concatenate_dicts(dict1, dict2):
    for key, value in dict2.items():
        dict1[key] = value
    
    return dict1

def index(request):
    def log_user(username, password):
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('favorites')
        else:
            # user does not exist
            pass
    
    errors = ''
    form = UserForm()
    showLogin = False
    showRegister = False

    if request.method == "POST":
        if "submitLogin" in request.POST:
            print('login')
            username = request.POST['loginUsername']
            password = request.POST['loginPassword']
            print(username, password)

            log_user(username, password)
        
        elif "submitRegister" in request.POST:
            print('register')
            form = UserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                print(username, raw_password)

                log_user(username, raw_password)
                
            else:
                errors = form.errors
                showRegister = True

    context = {
        'user_creation_form': form,
        'errors': errors,
        'showLogin': showLogin,
        'showRegister': showRegister
    }

    return render(request, 'index.html', concatenate_dicts(context, BASE_CONTEXT(request)))

@csrf_exempt
def show_exercise(request, exercise_title):
    print(exercise_title)
    ex = Exercise.objects.get(menu_option=MenuOption.objects.get(title=exercise_title))
    exercise_list = [s for s in str(ex.exercises).splitlines()]

    try:
        Favorite.objects.get(user=request.user, exercise=ex)
    except ObjectDoesNotExist:
        is_user_fav = False
    else:
        is_user_fav = True


    context = {
        "exercise": ex,
        "exercise_list": exercise_list,
        "is_user_fav": is_user_fav
    }

    return render(request, 'exercise.html', concatenate_dicts(context, BASE_CONTEXT(request)))

@csrf_exempt
def create_exercise(request, exercise_title):
    exercise_title = exercise_title.replace('_', ' ')
    context = { 
        'exercise_title': exercise_title,
    }

    if request.method == "POST":
        if "create-workout" in request.POST:
            youtube_code = request.POST.get('txt-youtube-code')
            exercises = request.POST.get('txt-excercises')
            remarks = request.POST.get('txt-remarks')

            Exercise(
                menu_option=MenuOption.objects.get(title=exercise_title),
                youtube_code=youtube_code,
                exercises=exercises,
                remarks=remarks,
            ).save()

            return show_exercise(request, exercise_title)
    
    return render(request, 'add_exercise.html', concatenate_dicts(context, BASE_CONTEXT(request)))

@csrf_exempt
def create_menu_option(request):
    parent_title = request.POST.get('parent_title')
    if parent_title == "":
        parent = None
    else:
        parent = MenuOption.objects.get(title=parent_title)
    title = request.POST.get('title')

    MenuOption(parent=parent, title=title).save()

    return redirect('index')

def logout_user(request):
    logout(request)

    return redirect('index')

@login_required(login_url='index')
def favorites(request):
    context = {
        'user_favs': Favorite.objects.filter(user=request.user)
    }
    return render(request, 'favorites.html', concatenate_dicts(context, BASE_CONTEXT(request)))

@csrf_exempt
def fav(request):
    exercise_title = request.POST['title']
    ex_obj = Exercise.objects.get(menu_option=MenuOption.objects.get(title=exercise_title))
    try:
        fav_obj = Favorite.objects.get(user=request.user, exercise=ex_obj)
    except ObjectDoesNotExist:
        Favorite(user=request.user, exercise=ex_obj).save()
        return HttpResponse('FAV[' + exercise_title + ']')
    else:
        fav_obj.delete()
        return HttpResponse('UNFAV [' + exercise_title + ']')
