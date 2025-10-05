from django.db import models

class Surah(models.Model):
    number = models.PositiveIntegerField(unique=True)
    name_ar = models.CharField(max_length=100)
    name_it = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name_plural = "Surah"
    
    def __str__(self):
        return f"{self.number}. {self.name_ar} ({self.name_it})"

class Ayah(models.Model):
    surah = models.ForeignKey(Surah, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ('surah', 'number')
        verbose_name_plural = "Ayah"
    
    def __str__(self):
        return f"{self.surah.number}:{self.number}"

class TafsirText(models.Model):
    ayah = models.ForeignKey(Ayah, on_delete=models.CASCADE, related_name='tafsir_texts')
    text_ar = models.TextField()  # testo del tafsir in arabo senza tashkeel
    text_tashkeel = models.TextField(blank=True, null=True)  # testo del tafsir in arabo con tashkeel
    
    class Meta:
        verbose_name_plural = "Tafsir Texts"
    
    def __str__(self):
        return f"Tafsir for {self.ayah}"

class TafsirTranslation(models.Model):
    tafsir_text = models.ForeignKey(TafsirText, on_delete=models.CASCADE, related_name='translations')
    arabic_selection = models.TextField()  # parte del testo arabo selezionato
    translation_it = models.TextField()    # traduzione italiana
    start_index = models.PositiveIntegerField()  # indice di inizio nel testo SENZA tashkeel
    end_index = models.PositiveIntegerField()    # indice di fine nel testo SENZA tashkeel
    start_index_tashkeel = models.PositiveIntegerField(default=0)  # indice di inizio nel testo CON tashkeel
    end_index_tashkeel = models.PositiveIntegerField(default=0)    # indice di fine nel testo CON tashkeel
    
    class Meta:
        unique_together = ('tafsir_text', 'start_index', 'end_index')
    
    def __str__(self):
        return f"Translation for {self.tafsir_text} [{self.start_index}:{self.end_index}]"