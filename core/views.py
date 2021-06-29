from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.auth import logout, authenticate, login

from core.forms import UserForm

from core.models import MenuOption, Exercise


def index(request):
    def log_user(username, password):
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("exist")
            return redirect('index')
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
        'menu_data': str(MenuOption.get_root_options_html()),
        'is_admin': request.user.is_superuser,
        'user_creation_form': form,
        'errors': errors,
        'showLogin': showLogin,
        'showRegister': showRegister
    }

    return render(request, 'index.html', context)

@csrf_exempt
def show_exercise(request):
    title = request.POST.get('exercise_title')
    print(request.POST)
    ex = Exercise.objects.get(menu_option=MenuOption.objects.get(title=title))
    obj = {
        'title': ex.menu_option.title,
        'youtube_link': ex.get_youtube_embed(),
        'exercise_list': ex.get_exercise_list(),
        'remarks': ex.remarks
    }

    return JsonResponse(obj)

@csrf_exempt
def create_exercise(request):
    title = request.POST.get('title')
    youtube_code = request.POST.get('youtube_code')
    exercises = request.POST.get('exercises')
    remarks = request.POST.get('remarks')
    print(title)

    Exercise(
        menu_option=MenuOption.objects.get(title=title),
        youtube_code=youtube_code,
        exercises=exercises,
        remarks=remarks,
    ).save()

    return HttpResponse("success")

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
