from django.contrib import admin
from .models import IPGInfo



class IPGInfoAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(IPGInfo, IPGInfoAdmin)