from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_tafsir/<int:surah_number>/<int:ayah_number>/', views.get_tafsir, name='get_tafsir'),
    path('save_translation/', views.save_translation, name='save_translation'),
    path('save_tashkeel/', views.save_tashkeel, name='save_tashkeel'),
]