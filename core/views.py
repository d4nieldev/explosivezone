from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser

from core.forms import UserForm, MenuOptionForm, ExerciseForm

from core.models import MenuOption, Exercise, Favorite


def BASE_CONTEXT(request):
    """
    provides the data needed for most functions

    :param request: request
    :return: dictionary with the fields: 'user_creation_form', 'menu_option_form', 'errors', 'showLogin',
     'showRegister', 'menu_data', 'is_admin', 'debug','login_error'
    """
    def log_user(username, password):
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return 'user_not_exist'

    errors = ''
    form = UserForm()
    showLogin = False
    showRegister = False    
    login_error = ''

    if request.method == "POST":
        if "submitLogin" in request.POST:
            # user requests to login
            username = request.POST['loginUsername']
            password = request.POST['loginPassword']

            if log_user(username, password) == 'user_not_exist':
                showLogin = True
                login_error = 'המשתמש לא קיים'
        
        elif "submitRegister" in request.POST:
            # user requests to register
            form = UserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')

                log_user(username, raw_password)
            else:
                errors = form.errors
                showRegister = True
        
        elif "submitAddOption" in request.POST:
            # admin requests to add new menu option
            menu_option_form = MenuOptionForm(request.POST)
            if menu_option_form.is_valid():
                menu_option_form.save()

    if not isinstance(request.user, AnonymousUser):  # a user is logged in
        user_favs = Favorite.objects.filter(user=request.user)
    else: 
        user_favs = None

    return dict({
        'user_creation_form': form,
        'menu_option_form': MenuOptionForm(),
        'errors': errors,  # errors of register modal
        'showLogin': showLogin,  # show login modal (bool)
        'showRegister': showRegister,  # show register modal (bool)
        'menu_data': str(MenuOption.get_root_options_html(request.user.is_superuser, user_favs)),  # menu html
        'is_admin': request.user.is_superuser,
        'debug': settings.DEBUG,
        'login_error': login_error  # errors of login modal
    })


def concatenate_dicts(dict1, dict2):
    """
    merges dict2 into dict1, overrides pre-existing values

    :param dict1: a dict to merge into
    :param dict2: a dict to merge into dict 1
    :return: dict1 U dict2
    """
    for key, value in dict2.items():
        dict1[key] = value
    
    return dict1


def index(request):
    return render(request, 'index.html', BASE_CONTEXT(request))


@csrf_exempt
def show_exercise(request, exercise_title):
    ex = Exercise.objects.get(menu_option=MenuOption.objects.get(title=exercise_title))

    # check if current exercise is a user favorite
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


@user_passes_test(lambda u: u.is_superuser)  # only super users can access this function
@csrf_exempt
def create_exercise(request, exercise_title):
    """
    Creates new exercise according to the form specified in forms.py

    :param request: request
    :param exercise_title: The title of new exercise to craete
    :return: if created exercise successfully, shows the new exercise. else, show the add exercise screen
    """
    exercise_title = exercise_title.replace('_', ' ')
        
    context = { 
        'exercise_title': exercise_title,
        'exercise_form': ExerciseForm()
    }

    if request.method == "POST":
        if "create-workout" in request.POST:
            exercise = Exercise(
                menu_option=MenuOption.objects.get(title=exercise_title),  # assign to corresponding menu option
                description=request.POST['description'],
                video_code=request.POST['video_code']
            )
            
            exercise.save()

            return show_exercise(request, exercise_title)
    
    return render(request, 'add_exercise.html', concatenate_dicts(context, BASE_CONTEXT(request)))


@user_passes_test(lambda u: u.is_superuser)  # only super users can access this function
@csrf_exempt
def create_menu_option(request):
    """
    Create a new menu option.

    :param request: request
    :return: refer to the homepage to load the new menu option
    """
    parent_title = request.POST.get('parent_title')
    if parent_title == "":
        parent = None
    else:
        parent = MenuOption.objects.get(title=parent_title)
    title = request.POST.get('title')

    MenuOption(parent=parent, title=title).save()

    return render(request, 'index.html', BASE_CONTEXT(request))


def logout_user(request):
    logout(request)

    return redirect('index')


@login_required(login_url='index')  # user has to be logged in to see favorites
def favorites(request):
    """
    :param request: request
    :return: Favorites view.
    """
    context = {
        'user_favs': Favorite.objects.filter(user=request.user)
    }
    return render(request, 'favorites.html', concatenate_dicts(context, BASE_CONTEXT(request)))


@login_required(login_url='index')  # user has to be logged in to make exercise favorite
@csrf_exempt
def fav(request):
    """
    Mark a specific exercise as favorite.
    :param request: request
    :return: FAV[exercise_title] if adding to favorites. else, UNFAV[exercise_title]
    """
    if request.method == "POST":
        exercise_title = request.POST['title']
        ex_obj = Exercise.objects.get(menu_option=MenuOption.objects.get(title=exercise_title))

        try:
            fav_obj = Favorite.objects.get(user=request.user, exercise=ex_obj)
        except ObjectDoesNotExist:
            # exercise is not in favorites - add it to favorites
            Favorite(user=request.user, exercise=ex_obj).save()
            return HttpResponse('FAV[' + exercise_title + ']')
        else:
            #  exercise is already a favorite - remove from favorites
            fav_obj.delete()
            return HttpResponse('UNFAV [' + exercise_title + ']')


@csrf_exempt
def discard_page(request):
    """
    Discards a specific page/exercise.
    :param request: request
    :return: "page discarded successfully" if page was discarded successfully
    """
    if request.method == "POST":
        MenuOption.objects.get(id=request.POST['id']).delete()
        return HttpResponse('page discarded successfully')
