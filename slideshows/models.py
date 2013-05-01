# -*- coding: utf-8 -*-
"""
Modèles de données
"""
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from tinymce import models as tinymce_models

from .utils import content_file_name

IMAGE_FILE_UPLOADTO = lambda x,y: content_file_name('sliders/slides/%Y/%m/%d', x, y)

class Slideshow(models.Model):
    """
    Slideshow that contains slides
    """
    created = models.DateTimeField(_('created'), blank=True, editable=False)
    title = models.CharField(_('title'), blank=False, max_length=255)

class Slide(models.Model):
    """
    Slide item
    """
    slideshow = models.ForeignKey(Slideshow, verbose_name=_('slideshow'), blank=False)
    created = models.DateTimeField(_('created'), blank=True, editable=False)
    title = models.CharField(_('title'), blank=False, max_length=255)
    priority = models.IntegerField(_('display priority'), default=100, help_text=_('Set this value to 0 will hide the item'))
    content = tinymce_models.HTMLField(_("content"), blank=False)
    image = models.ImageField(_('image'), upload_to=IMAGE_FILE_UPLOADTO, max_length=255, blank=False)

    def __unicode__(self):
        return self.title

    @property
    def get_file(self):
        try:
            return self.image.url
        except ValueError:
            return None

    def clean(self):
        if not self.get_file:
            raise ValidationError(_('Please fill an image'))

    def save(self, *args, **kwargs):
        # First create
        if not self.created:
            self.created = datetime.datetime.now()
        
        super(Slide, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Slide")
        verbose_name_plural = _("Slides")
