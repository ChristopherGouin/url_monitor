from django.db import models

from users.models import BaseModel, UserProfile

# Create your models here.
class Url(BaseModel):
     name = models.CharField(
          verbose_name="Nom du site",
          max_length=100,
          blank=True,
          null=True,
     )

     url = models.URLField(
          verbose_name="Url à controler",
          blank=False,
          null=False,
     )

     description = models.TextField(
          verbose_name="Description",
          max_length=250,
          blank=True,
          null=True,
     )

     http_code = models.IntegerField(
          verbose_name="Code de réponse HTTP attendu",
          blank=True,
          null=True,
          help_text="Laisser vide pour ne pas tester",
     )

     display_time = models.IntegerField(
          verbose_name="Temps d'affichage maximum attendu (ms)",
          blank=True,
          null=True,
          help_text="Laisser vide pour ne pas tester",
     )

     is_content_empty = models.BooleanField(
          verbose_name="la réponse doit-elle contenir du text ?",
     )

     ssl_expiration = models.IntegerField(
          verbose_name="Durée minimal d'expiration (jours)",
          blank=True,
          null=True,
          help_text="Le test sera ok si le certificat ssl expire dans plus de jours que cette durée. Laisser vide pour ne pas tester",
     )

     is_auto_check = models.BooleanField(
          verbose_name="Vérification automatique",
          default=True,
          help_text="la vérification sera lancée par le script",
     )

     is_mail_report = models.BooleanField(
          verbose_name="Rapport par mail",
          default=False,
     )

     user = models.ForeignKey(
          UserProfile,
          on_delete=models.SET_NULL,
          db_index=True,
          null=True,
          blank=True,
          default=None,
     )

     def __str__(self):
          if self.name:
               return self.name
          else:
               return self.url

     class Meta:
          verbose_name="Url"
          verbose_name_plural="Urls"

