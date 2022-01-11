
# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

CURRENCY = settings.CURRENCY

def validate_positive_number(value):
    if value < 0 :
        raise ValidationError('This number is lower than 0!')
    return value


class Category(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(unique=True, max_length=150)

    def __str__(self):
        return self.title


class Product(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(unique=True, max_length=150)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    value = models.DecimalField(decimal_places=2, max_digits=10, default=0, validators=[validate_positive_number,])

    def __str__(self):
        return f'{self.title}'

    def tag_value(self):
        return f'{self.value} {CURRENCY}'

    def tag_category(self):
        return f'{self.category.title}'