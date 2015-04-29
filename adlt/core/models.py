from django.db import models
from django.utils.translation import ugettext_lazy as _


class Organization(models.Model):
    title = models.CharField(_("Pavadinimas"), max_length=255)

    def __str__(self):
        return self.title


class Dataset(models.Model):
    OPEN_LICENCE = 1
    STRUCTURED_DATA = 2
    OPEN_FORMAT = 3
    USES_URIS = 4
    LINKED_DATA = 5
    MATURITY_LEVEL_CHOICES = (
        (OPEN_LICENCE, _('1. Atvira licencija')),
        (STRUCTURED_DATA, _('2. Struktūruoti duomenys')),
        (OPEN_FORMAT, _('3. Atviras formatas')),
        (USES_URIS, _('4. Adresuojami duomenys')),
        (LINKED_DATA, _('5. Susietieji duomenys')),
    )

    title = models.CharField(_("Pavadinimas"), max_length=255)
    organization = models.ForeignKey(
        Organization,
        verbose_name=_("Organizacija"),
        help_text=_("Oranizacija teikianti duomenis."),
    )
    description = models.TextField(_("Aprašymas"))
    maturity_level = models.PositiveSmallIntegerField(
        _("Brandos lygis"),
        choices=MATURITY_LEVEL_CHOICES,
    )
    link = models.URLField(_("Nuoroda"), help_text=_(
        "Nuoroda į vietą internete, kur pateikiami duomenys ar informacija "
        "apie duomenis."
    ))


class Project(models.Model):
    title = models.CharField(_("Pavadinimas"), max_length=255)
    description = models.TextField(_("Aprašymas"))
    datasets_links = models.TextField(_("Duomenų šaltiniai"))
    datasets = models.ManyToManyField(Dataset)
