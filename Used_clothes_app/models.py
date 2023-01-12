from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.name}'


class Institution(models.Model):
    choice = (
        ('f', 'fundacja'),
        ('o.p', 'organizacja pozarzadowa'),
        ('z.l', 'zbiórka lokalna'),
    )
    name = models.CharField(max_length=128)
    description = models.TextField()
    type = models.CharField(max_length=3, choices=choice, default='z.l')

    def __str__(self):
        return f'{self.name}, {self.description}, {self.type}'


class User(AbstractUser):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)


class Donation(models.Model):
    quantity = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    phone_number = models.PositiveIntegerField()
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=5)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)