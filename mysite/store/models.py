from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

def redimensionar_imagen(image):
    img = Image.open(image)
    max_cm = 10
    dpi = img.info.get('dpi', (72, 72))  # Suponiendo una resolución estándar de 72 DPI
    max_px = max_cm * (dpi[0] / 2.54)  # Convertir cm a píxeles

    if img.width > max_px or img.height > max_px:
        img.thumbnail((max_px, max_px), Image.LANCZOS)
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=90)
        output.seek(0)
        return InMemoryUploadedFile(output, 'ImageField', f"{image.name.split('.')[0]}.jpg", 'image/jpeg', output.getbuffer().nbytes, None)
    return image

class Articulo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='imagenes/', validators=[redimensionar_imagen])

    def save(self, *args, **kwargs):
        # Redimensionar la imagen si es necesario
        if self.imagen:
            self.imagen = redimensionar_imagen(self.imagen)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
