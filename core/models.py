from django.db import models

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField


class MenuOption(models.Model):
    """
    A menu option is a category or link to exercise.
    """
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50, unique=True)

    def get_children(self):
        """
        get a list of children menu options.

        :return: list of menu options that are under self in the hierarchy
        """
        all_options = MenuOption.objects.all()
        children = []

        for opt in all_options:
            if opt.parent == self:
                children.append(opt)

        return children

    def get_html(self, admin_view, user_favs):
        """
        Html string builder for the menu option.

        :param admin_view: true if there are admin privileges to see hidden menu options.
        :param user_favs: list of favorite menu options.
        :return: html string of the menu option and it's children.
        """
        children = self.get_children()
        children_html = ''.join([child.get_html(admin_view, user_favs) for child in children])
        title = str(self.title).replace(' ', '_')

        # if there are children create button as collapsable and add the children as it's options and return immediately
        if len(children):
            return f"""
            <li>
                <button data-bs-target='#{title}Submenu' type='button' data-bs-toggle='collapse' aria-expanded='false' 
                        class='dropdown-toggle'>
                    {self.title}
                </button>
                <ul class='collapse list-unstyled' id='{title}Submenu'>
                    {children_html}
                </ul>
            </li>
            """

        # there are no children - base case.
        fav_addition = "d-none"
        if user_favs:
            for fav in user_favs:
                if fav.exercise.menu_option.title == self.title:
                    fav_addition = ""
                    break

        # create button for this menu option
        base_html = f"""
        <li>
            <button type='button' data-sendto='{self.title}' class='exercise'>
                {self.title}<i class='fas fa-star text-warning fa-2x {fav_addition}'></i>
            </button>
        </li>
        """

        try:
            Exercise.objects.get(menu_option=self)  # try to get children
        except ObjectDoesNotExist:  # no children
            if admin_view:
                # add delete button and add button at the end of each category.
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
        else:  # at least one child
            if admin_view:
                # add delete button (for whole category)
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

    @staticmethod
    def get_root_options_html(admin_view, user_favs):
        """
        Combines all html of all menu options.

        :param admin_view: true if there are admin privileges to see hidden menu options.
        :param user_favs: list of favorite menu options.
        :return: full menu of choices.
        """
        all_options = MenuOption.objects.all()
        root_options_html = ""

        for opt in all_options:
            if not opt.parent:
                root_options_html += opt.get_html(admin_view, user_favs)
        
        return root_options_html

    def __str__(self):
        if self.parent:
            return str(self.parent) + '>' + self.title
        else:
            return self.title


class Exercise(models.Model):
    """
    An exercise is a page that is not the homepage.
    """
    menu_option = models.ForeignKey(MenuOption, on_delete=models.CASCADE)
    description = RichTextField(blank=True, null=True, config_name="awesome_ckeditor")
    video_code = models.CharField(max_length=15, default='')

    def __str__(self):
        return self.menu_option.title


class Favorite(models.Model):
    """
    if an exercise is here, it is one of connected user's favorite exercises.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.user}] ★ {self.exercise}'
