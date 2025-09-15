from django.contrib import admin
from .models import (
    Surah, Ayah,
    TafsirText, TafsirTranslation
)

admin.site.register(Surah)
admin.site.register(Ayah)
admin.site.register(TafsirText)
admin.site.register(TafsirTranslation)