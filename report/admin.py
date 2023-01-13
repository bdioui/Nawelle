from django.contrib import admin
from .models import import_dossiers, dossier, Note, Notification
# Register your models here.
admin.site.register(import_dossiers)
admin.site.register(dossier)
admin.site.register(Note)
admin.site.register(Notification)


