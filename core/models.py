from django.db import models

class MenuOption(models.Model):
    parent = models.ForeignKey('MenuOption', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
