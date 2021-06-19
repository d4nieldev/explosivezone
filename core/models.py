from django.db import models

class MenuOption(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)

    def get_children(self):
        all_options = MenuOption.objects.all()
        children = []

        print(all_options)
