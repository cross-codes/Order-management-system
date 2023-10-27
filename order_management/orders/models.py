from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    PRIORITY_CHOICES = (("LOW", "Low"), ("MEDIUM", "Medium"), ("HIGH", "High"))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    desc = models.TextField()
    date = models.DateField()
    pr_tag = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="MEDIUM")

    def __str__(self):
        return self.title
