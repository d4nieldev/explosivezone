from django.shortcuts import render
from django.http import HttpResponse

from core.models import MenuOption 

def index(request):
    context = {
        'menu_data': str(MenuOption.get_root_options_html())
    }
    print(context['menu_data'])
    return render(request, 'index.html', context)
