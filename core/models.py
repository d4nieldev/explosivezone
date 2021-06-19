from django.db import models

from core.html_builder import HtmlTag

class MenuOption(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50, unique=True)

    @staticmethod
    def get_root_options_html():
        all_options = MenuOption.objects.all()
        root_options_html = ""

        for opt in all_options:
            if not opt.parent:
                root_options_html += opt.get_html()
        
        return root_options_html


    def get_children(self):
        all_options = MenuOption.objects.all()
        children = []

        for opt in all_options:
            if opt.parent == self:
                children.append(opt)

        return children
    

    def get_html(self):
        children = self.get_children()
        children_html = ''.join([child.get_html() for child in children])
        
        if len(children):
            a_attrs = {
                'href': f'#{self.title}Submenu', 
                'data-bs-toggle': 'collapse', 
                'aria-expanded': 'false', 
                'class': 'dropdown-toggle',
            }
            ul_attrs = {
                'class': 'collapse lisst-unstyled',
                'id': f'{self.title}Submenu',
            }

            return str(
            HtmlTag('li', 
            content=str(HtmlTag('a', a_attrs, self.title)) +
            str(HtmlTag('ul', ul_attrs, content=children_html)))
            )
        return str(
            HtmlTag('li', 
            content=HtmlTag('a', {'href': '{% url ' + str(self.title).lower() + ' %}'}, self.title))
            )
    

    def __str__(self):
        if self.parent:
            return str(self.pk) + ":" + self.parent.title + '>' + self.title
        else:
            return str(self.pk) + ":" + self.title
