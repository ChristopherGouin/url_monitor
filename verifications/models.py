from django.db import models

from users.models import BaseModel
from urls.models import Url

class Verification(BaseModel):
    url = models.ForeignKey(
        Url,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )

    http_code = models.IntegerField(
        verbose_name="Code reponse HTPP",
        blank=False,
        null=False,
    )

    display_time = models.IntegerField(
        verbose_name="Temps d'affichage",
        blank=False,
        null=False
    )

    is_content_empty = models.BooleanField(
        verbose_name="contenu de la réponse vide",
        blank=True,
        null=True,
    )

    ssl_expiration_date = models.DateTimeField(
        verbose_name="date d'expiration du certificat",
        blank=True,
        null=True,
    )

    result = models.BooleanField(
        verbose_name="résultat global du test",
        default=False,
        blank=False,
        null=False
    )

    description = models.TextField(
        verbose_name="Description du résultat de la vérification",
        blank=True,
        null=True
    )

    def __str__(self):
        return "%s - %s" % (self.created.strftime('%Y-%m-%d %H:%M'), str(self.url))

    def status(self):
        if self.result:
            return "Succès"
        else:
            return "Echec"

    def content(self):
        if self.is_content_empty:
            return "Oui"
        else:
            return "Non"

    class Meta:
        verbose_name="Vérification"
        verbose_name_plural="Vérifications"