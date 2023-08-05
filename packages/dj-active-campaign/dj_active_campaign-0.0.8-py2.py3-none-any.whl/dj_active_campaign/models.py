import uuid

from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.utils.translation import gettext_lazy as _

def set_default_site_id():
    return Site.objects.get_current()


class CustomFieldTypes(models.TextChoices):
    CHECKBOX  = 'checkbox', _("Checkbox")
    DATE      = 'date', _("Date")
    DATETIME  = 'datetime', _("Datetime")
    DROPDOWN  = 'dropdown', _("Dropdown")
    HIDDEN    = 'hidden', _("Hidden")
    LIST_BOX  = 'listbox', _("List Box")
    NULL      = 'NULL', _("Null")
    RADIO     = 'radio', _('Radio')
    TEXT      = 'text', _("Text")
    TEXT_AREA = 'textarea', _("Text Area")


class CustomField(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    site = models.ForeignKey(Site, verbose_name=_("Site"), on_delete=models.CASCADE, default=set_default_site_id, related_name="ac_custom_field")
    ac_id = models.CharField(_("Active Campaign ID"), max_length=50, blank=True, null=True, default="-")
    ac_title = models.CharField(_("Field Title"), max_length=50)
    ac_value = models.JSONField(_("Field Value"), default=None, blank=True, null=True)
    ac_type = models.CharField(_("Field Type"), max_length=50, choices=CustomFieldTypes.choices, default=CustomFieldTypes.TEXT)
    required = models.BooleanField(_("Required"), default=False)
    meta = models.JSONField(_("Meta"), default=None, blank=True, null=True)

    objects = models.Manager()
    on_site = CurrentSiteManager()


    class Meta:
        verbose_name = "Custom Field"
        verbose_name_plural = "Custom Fields"

    def __str__(self):
        return self.ac_title

