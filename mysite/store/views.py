from django.shortcuts import render, redirect
from .models import Articulo
from .forms import ArticuloForm

def lista_articulos(request):
    articulos = Articulo.objects.all()
    return render(request, 'store/lista_articulos.html', {'articulos': articulos})

def crear_articulo(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_articulos')
    else:
        form = ArticuloForm()
    return render(request, 'store/formulario_articulo.html', {'form': form})
