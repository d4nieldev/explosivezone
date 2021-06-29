from django.db import models

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from core.html_builder import HtmlTag

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
            base_html = HtmlTag(
                'li', content=HtmlTag('button', {'type': 'button', 'data-sendTo': self.title, 'class': 'exercise'}, self.title + 
                str(HtmlTag('i', attributes={"class": "fas fa-star text-warning fa-2x"})))
            )
        else:
            base_html = HtmlTag(
                'li', content=HtmlTag('button', {'type': 'button', 'data-sendTo': self.title, 'class': 'exercise'}, self.title + 
                str(HtmlTag('i', attributes={"class": "fas fa-star text-warning fa-2x d-none"})))
            )
        
        if len(children):
            button_attrs = {
                'data-bs-target': f'#{title}Submenu', 
                'type': 'button',
                'data-bs-toggle': 'collapse', 
                'aria-expanded': 'false', 
                'class': 'dropdown-toggle',
            }
            ul_attrs = {
                'class': 'collapse list-unstyled',
                'id': f'{title}Submenu',
            }

            return str(
            HtmlTag('li', 
            content=str(HtmlTag('button', button_attrs, self.title)) +
            str(HtmlTag('ul', ul_attrs, content=children_html)))
            )
        
        try:
            exercise = Exercise.objects.get(menu_option=self)
        except ObjectDoesNotExist:
            if admin_view:
                base_html = HtmlTag('li', 
                content=HtmlTag('button', {'type': 'button', 'data-sendTo': title, 'data-new':'true', 'class': 'exercise'}, self.title + 
                str(HtmlTag('a', {'data-del': self.pk, 'class': 'remove-page ms-5'}, "<center><i class='fas fa-trash'></i></center>")) +
                str(HtmlTag('a', {'class': 'add-page'}, "<i class='fas fa-plus'></i>"))))
            else:
                base_html = ''
        else:
            if admin_view:
                base_html = HtmlTag('li', 
                content=HtmlTag('button', {'type': 'button', 'data-sendTo': title, 'class': 'exercise'}, self.title + 
                str(HtmlTag('a', {'data-del': self.pk, 'class': 'remove-page'}, "<center><i class='fas fa-trash'></i></center>"))))
            
        return str(base_html)
    

    def __str__(self):
        if self.parent:
            return str(self.pk) + ":" + self.parent.title + '>' + self.title
        else:
            return str(self.pk) + ":" + self.title

class Exercise(models.Model):
    menu_option = models.ForeignKey(MenuOption, on_delete=models.CASCADE)
    youtube_code = models.CharField(max_length=150)
    exercises = models.TextField()
    remarks = models.TextField()

    @property
    def get_youtube_embed(self):
        return "https://www.youtube.com/embed/" + self.youtube_code

    def get_exercise_list(self):
        lst = str(self.exercises).splitlines()
        lst = [s for s in lst if s != ""]
            
        return lst

    def __str__(self):
        return self.menu_option.title

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.user}] ★ {self.exercise}'
