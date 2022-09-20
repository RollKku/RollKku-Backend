from django.db import models
from User.models import User
from Deco.models import Deco


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deco = models.ForeignKey(Deco, on_delete=models.CASCADE)

    def __str__(self):
        return self.user
