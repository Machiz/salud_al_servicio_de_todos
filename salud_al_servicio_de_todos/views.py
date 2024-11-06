# grafo_app/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from . import grafo

def main_view(request):
    # Esta vista renderiza la plantilla HTML para mostrar el grafo
    return render(request, 'index.html')
def graph(request):
    # Esta vista genera y retorna los datos del grafo en formato JSON
    grafo.dibujoGrafo()
    return JsonResponse(grafo.dibujoGrafo())
