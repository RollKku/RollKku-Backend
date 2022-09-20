import os
import uuid

from django.db import models
from User.models import User
from Category.models import Category
from Variable.models import Variable


def deco_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('media/', filename)


class Deco(models.Model):
    name = models.CharField(max_length=20)
    thumbnail = models.ImageField(upload_to=deco_image_file_path, null=True, blank=True)
    css = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='decos')
    variables = models.ManyToManyField(Variable, related_name='decos')

    def __str__(self):
        return self.name
