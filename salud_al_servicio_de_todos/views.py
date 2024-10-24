# grafo_app/views.py
import json
import networkx as nx
from django.shortcuts import render
from django.http import JsonResponse
import grafo

def grafo_view(request):
    # Esta vista renderiza la plantilla HTML para mostrar el grafo
    return render(request, 'Paginas\index.html')

def graph(request):
    # Esta vista genera y retorna los datos del grafo en formato JSON
    grafo.dibujoGrafo()
    return JsonResponse(grafo.dibujoGrafo())
