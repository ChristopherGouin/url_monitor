from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add = True, verbose_name="Date de création")
    modified = models.DateTimeField(auto_now = True, verbose_name="Date de modification")

    class Meta:
        abstract = True
        ordering = ("-created", )

class UserProfile(AbstractUser, BaseModel):

    display_name = models.CharField(
        verbose_name= "Nom d'affichage",
        max_length=100,
        default=None,
        blank=True,
        null=True
    )

    def __str__(self):
        if self.display_name :
            return self.display_name
        else:
            return self.username

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering= ("created", )
