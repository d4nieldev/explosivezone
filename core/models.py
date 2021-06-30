from django.db import models

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from core.html_builder import HtmlTag

from ckeditor.fields import RichTextField

class MenuOption(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50, unique=True)

    @staticmethod
    def get_root_options_html(admin_view, user_favs):
        all_options = MenuOption.objects.all()
        root_options_html = ""

        for opt in all_options:
            if not opt.parent:
                root_options_html += opt.get_html(admin_view, user_favs)
        
        return root_options_html


    def get_children(self):
        all_options = MenuOption.objects.all()
        children = []

        for opt in all_options:
            if opt.parent == self:
                children.append(opt)

        return children
    

    def get_html(self, admin_view, user_favs):
        children = self.get_children()
        children_html = ''.join([child.get_html(admin_view, user_favs) for child in children])
        title = str(self.title).replace(' ', '_')

        is_fav = False
        if user_favs:
            for fav in user_favs:
                if fav.exercise.menu_option.title == self.title:
                    is_fav = True
                    break

        if is_fav:
            base_html = f"""
            <li>
                <button type='button' data-sendto='{self.title}' class='exercise'>
                    {self.title}<i class='fas fa-star text-warning fa-2x'></i>
                </button>
            </li>
            """
        else:
            base_html = f"""
            <li>
                <button type='button' data-sendto='{self.title}' class='exercise'>
                    {self.title}<i class='fas fa-star text-warning fa-2x d-none'></i>
                </button>
            </li>
            """
        
        if len(children):
            return f"""
            <li>
                <button data-bs-target='#{title}Submenu' type='button' data-bs-toggle='collapse' aria-expanded='false' class='dropdown-toggle'>{self.title}</button>
                <ul class='collapse list-unstyled' id='{title}Submenu'>
                    {children_html}
                </ul>
            </li>
            """
        
        try:
            exercise = Exercise.objects.get(menu_option=self)
        except ObjectDoesNotExist:
            if admin_view:
                base_html = f"""
                <li>
                    <button type='button' data-sendto='{title}' data-new='true' class='exercise'>
                        {self.title}
                    </button>
                    <a data-del='{self.pk}' class='remove-page ms-5'>
                        <center><i class='fas fa-trash'></i></center>
                    </a>
                    <a class='add-page'>
                        <i class='fas fa-plus'></i>
                    </a>
                    
                </li>
                """
            else:
                base_html = ''
        else:
            if admin_view:
                base_html = f"""
                <li>
                    <button type='button' data-sendto='{title}' class='exercise'>
                        {self.title}
                    </button>
                    <a data-del='{self.pk}' class='remove-page'>
                        <center><i class='fas fa-trash'></i></center>
                    </a>
                    
                </li>
                """
            
        return base_html
    

    def __str__(self):
        if self.parent:
            return str(self.parent) + '>' + self.title
        else:
            return self.title

class Exercise(models.Model):
    menu_option = models.ForeignKey(MenuOption, on_delete=models.CASCADE)
    description = RichTextField(blank=True, null=True, config_name="awesome_ckeditor")
    video_code = models.CharField(max_length=15, default='')

    def __str__(self):
        return self.menu_option.title

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.user}] ★ {self.exercise}'
