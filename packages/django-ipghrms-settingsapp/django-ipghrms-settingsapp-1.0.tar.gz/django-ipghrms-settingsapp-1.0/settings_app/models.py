from django.db import models
from settings_app.upload_utils import upload_logo, upload_cop
from django.contrib.auth.models import User
# Create your models here.


class ActiveInfoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class IPGInfo(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to=upload_logo, null=True)
    cop = models.ImageField(default='default.jpg', upload_to=upload_cop, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    municipality = models.CharField(max_length=100, null=True, blank=True, verbose_name="Municipio no Nasaun")
    mobile = models.CharField(max_length=20, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=False, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    objects = models.Manager() # The default manager
    active = ActiveInfoManager() # The custom manager

    def save(self, *args, **kwargs):
        if self.is_active:
            # If the current instance is set to active, make all others inactive
            IPGInfo.objects.exclude(id=self.id).update(is_active=False)
            
        super().save(*args, **kwargs)
    def __str__(self):
        template = '{0.title}-{0.is_active}'
        return template.format(self)

