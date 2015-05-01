import autoslug

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class Agent(models.Model):
    slug = autoslug.AutoSlugField(populate_from='title', unique=True)
    title = models.CharField(_("Pavadinimas/Vardas"), max_length=255)
    individual = models.BooleanField(default=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Dataset(models.Model):
    NO_DATA = 0
    OPEN_LICENCE = 1
    STRUCTURED_DATA = 2
    OPEN_FORMAT = 3
    USES_URIS = 4
    LINKED_DATA = 5
    MATURITY_LEVEL_CHOICES = (
        (NO_DATA, _('0. Duomenys nėra pateikti')),
        (OPEN_LICENCE, _('1. Atvira licencija')),
        (STRUCTURED_DATA, _('2. Struktūruoti duomenys')),
        (OPEN_FORMAT, _('3. Atviras formatas')),
        (USES_URIS, _('4. Adresuojami duomenys')),
        (LINKED_DATA, _('5. Susietieji duomenys')),
    )

    slug = autoslug.AutoSlugField(populate_from='title', unique_with='agent')
    title = models.CharField(_("Pavadinimas"), max_length=255)
    agent = models.ForeignKey(Agent, verbose_name=_("Organizacija"))
    description = models.TextField(_("Aprašymas"))
    maturity_level = models.PositiveSmallIntegerField(_("Brandos lygis"), choices=MATURITY_LEVEL_CHOICES)
    link = models.URLField(_("Nuoroda"), help_text=_(
        "Nuoroda į vietą internete, kur pateikiami duomenys ar informacija "
        "apie duomenis."
    ))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('dataset-details', args=[self.agent.slug, self.slug])


class Project(models.Model):
    slug = autoslug.AutoSlugField(populate_from='title', unique_with='agent')
    title = models.CharField(_("Pavadinimas"), max_length=255)
    agent = models.ForeignKey(Agent, verbose_name=_("Organizacija/Asmnuo"))
    description = models.TextField(_("Aprašymas"))
    datasets_links = models.TextField(_("Duomenų šaltiniai"))
    datasets = models.ManyToManyField(Dataset)

    def __str__(self):
        return self.title
