from django import forms
from .models import Articulo
from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['nombre', 'descripcion', 'precio', 'imagen']

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            img = Image.open(imagen)
            max_cm = 10
            dpi = img.info.get('dpi', (72, 72))  # Suponiendo una resolución estándar de 72 DPI
            max_px = max_cm * (dpi[0] / 2.54)  # Convertir cm a píxeles

            if img.width > max_px or img.height > max_px:
                img.thumbnail((max_px, max_px), Image.LANCZOS)
                output = io.BytesIO()
                img.save(output, format='JPEG', quality=90)
                output.seek(0)
                imagen = InMemoryUploadedFile(output, 'ImageField', f"{imagen.name.split('.')[0]}.jpg", 'image/jpeg', output.getbuffer().nbytes, None)
        return imagen
