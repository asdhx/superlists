from django.db import models

class List(models.Model):
    name = models.CharField(max_length=100)



class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)
