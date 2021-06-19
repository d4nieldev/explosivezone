from django.db import models

from core.html_builder import HtmlTag

class MenuOption(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50)


    def get_children(self):
        all_options = MenuOption.objects.all()
        children = []

        for opt in all_options:
            if opt.parent == self:
                children.append(opt)

        return children
    

    def get_html(self):
        children = self.get_children()
        
        if len(children):
            return "has children"
        return str(HtmlTag('li', content=HtmlTag('a', {'href': '{% url ' + str(self.title).lower() + ' %}'}, self.title)))
    

    def __str__(self):
        children = self.get_children()

        if len(children):
            children_titles = [child.title for child in children]
            children_str = ', '.join(children_titles)
            return self.title + '>' + children_str

        else:
            return self.title
