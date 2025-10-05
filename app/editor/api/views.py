from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import re

from editor.models import Surah, Ayah, TafsirText, TafsirTranslation
from pytafseer import QuranTafseer

tafseer = QuranTafseer(book_id=3)  # activate tafseer book

def index(request):
    surahs = Surah.objects.all().order_by('number')
    return render(request, 'index.html', {'surahs': surahs})

def get_tafsir(request, surah_number, ayah_number):
    
    verse_tafseer = tafseer.get_verse_tafseer(
        chapter_number=surah_number,
        verse_number=ayah_number
    )
    
    tafseer_text = verse_tafseer.get('text', '')

    surah, created = Surah.objects.get_or_create(number=surah_number)
    ayah, created = Ayah.objects.get_or_create(surah=surah, number=ayah_number)
    
    # Ottieni o crea il testo del tafsir per questa ayah
    tafsir_text, created = TafsirText.objects.get_or_create(
        ayah=ayah,
        defaults={
            'text_ar': f"{tafseer_text}",
            'text_tashkeel': ''  # Inizialmente vuoto
        }
    )
    
    # Prepara le traduzioni esistenti
    translations = []
    for trans in tafsir_text.translations.all():
        translations.append({
            'start': trans.start_index,
            'end': trans.end_index,
            'start_tashkeel': trans.start_index_tashkeel,
            'end_tashkeel': trans.end_index_tashkeel,
            'text': trans.translation_it
        })
    
    return JsonResponse({
        'text_ar': tafsir_text.text_ar,
        'text_tashkeel': tafsir_text.text_tashkeel or '',
        'translations': translations
    })

@csrf_exempt
@require_POST
def save_translation(request):
    data = json.loads(request.body)
    
    surah_number = data.get('surah')
    ayah_number = data.get('ayah')
    arabic_selection = data.get('arabic_selection')
    translation_it = data.get('translation_it')
    start_index = data.get('start_index')  # Indici per testo SENZA tashkeel
    end_index = data.get('end_index')
    # start_index_tashkeel = data.get('start_index_tashkeel')  # Indici per testo CON tashkeel
    # end_index_tashkeel = data.get('end_index_tashkeel')
    
    surah = get_object_or_404(Surah, number=surah_number)
    ayah = get_object_or_404(Ayah, surah=surah, number=ayah_number)
    tafsir_text = get_object_or_404(TafsirText, ayah=ayah)
    
    # Salva entrambe le versioni degli indici
    translation, created = TafsirTranslation.objects.update_or_create(
        tafsir_text=tafsir_text,
        start_index=start_index,
        end_index=end_index,
        defaults={
            'arabic_selection': arabic_selection,
            'translation_it': translation_it,
            # 'start_index_tashkeel': start_index_tashkeel,
            # 'end_index_tashkeel': end_index_tashkeel
        }
    )
    
    return JsonResponse({'status': 'success'})

@csrf_exempt
@require_POST
def save_tashkeel(request):
    data = json.loads(request.body)
    
    surah_number = data.get('surah')
    ayah_number = data.get('ayah')
    text_tashkeel = data.get('text_tashkeel')
    
    surah = get_object_or_404(Surah, number=surah_number)
    ayah = get_object_or_404(Ayah, surah=surah, number=ayah_number)
    tafsir_text = get_object_or_404(TafsirText, ayah=ayah)
    
    # Aggiorna il testo con tashkeel
    tafsir_text.text_tashkeel = text_tashkeel
    tafsir_text.save()
    
    return JsonResponse({'status': 'success'})