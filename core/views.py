from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser

from core.forms import UserForm, MenuOptionForm, ExerciseForm

from core.models import MenuOption, Exercise, Favorite


def BASE_CONTEXT(request):
    def log_user(username, password):
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('favorites')
        else:
            # user does not exist
            return 'user_not_exist'

    errors = ''
    form = UserForm()
    showLogin = False
    showRegister = False    
    login_error = ''

    if request.method == "POST":
        if "submitLogin" in request.POST:
            username = request.POST['loginUsername']
            password = request.POST['loginPassword']
            print(username, password)

            if log_user(username, password) == 'user_not_exist':
                showLogin = True
                login_error = 'המשתמש לא קיים'
        
        elif "submitRegister" in request.POST:
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
        
        elif "submitAddOption" in request.POST:
            menu_option_form = MenuOptionForm(request.POST)
            if menu_option_form.is_valid():
                menu_option_form.save()

    if not isinstance(request.user, AnonymousUser):
        user_favs = Favorite.objects.filter(user=request.user)
    else: 
        user_favs = None

    return dict({
        'user_creation_form': form,
        'menu_option_form': MenuOptionForm(),
        'errors': errors,
        'showLogin': showLogin,
        'showRegister': showRegister,
        'menu_data': str(MenuOption.get_root_options_html(request.user.is_superuser, user_favs)),
        'is_admin': request.user.is_superuser,
        'debug': settings.DEBUG,
        'login_error': login_error
    })

def concatenate_dicts(dict1, dict2):
    for key, value in dict2.items():
        dict1[key] = value
    
    return dict1

def index(request):
    return render(request, 'index.html', BASE_CONTEXT(request))

@csrf_exempt
def show_exercise(request, exercise_title):
    ex = Exercise.objects.get(menu_option=MenuOption.objects.get(title=exercise_title))

    try:
        if not isinstance(request.user, AnonymousUser):
            Favorite.objects.get(user=request.user, exercise=ex)
    except ObjectDoesNotExist:
        is_user_fav = False
    else:
        is_user_fav = True


    context = {
        "exercise": ex,
        "is_user_fav": is_user_fav
    }

    return render(request, 'exercise.html', concatenate_dicts(context, BASE_CONTEXT(request)))

@user_passes_test(lambda u: u.is_superuser)
@csrf_exempt
def create_exercise(request, exercise_title):
    exercise_title = exercise_title.replace('_', ' ')
        
    context = { 
        'exercise_title': exercise_title,
        'exercise_form': ExerciseForm()
    }

    if request.method == "POST":
        if "create-workout" in request.POST:
            exercise = Exercise(
                menu_option=MenuOption.objects.get(title=exercise_title), 
                description=request.POST['description'],
                video_code=request.POST['video_code']
            )
            
            exercise.save()

            return show_exercise(request, exercise_title)
    
    return render(request, 'add_exercise.html', concatenate_dicts(context, BASE_CONTEXT(request)))

@user_passes_test(lambda u: u.is_superuser)
@csrf_exempt
def create_menu_option(request):
    parent_title = request.POST.get('parent_title')
    if parent_title == "":
        parent = None
    else:
        parent = MenuOption.objects.get(title=parent_title)
    title = request.POST.get('title')

    MenuOption(parent=parent, title=title).save()

    return render(request, 'index', BASE_CONTEXT(request))

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
    
@csrf_exempt
def discard_page(request):
    MenuOption.objects.get(id=request.POST['id']).delete()
    return HttpResponse('page discarded successfully')
