from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150)


class Task(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)


