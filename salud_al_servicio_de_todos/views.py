# grafo_app/views.py
import json
import networkx as nx
from django.shortcuts import render
from django.http import JsonResponse

def grafo_view(request):
    # Esta vista renderiza la plantilla HTML para mostrar el grafo
    return render(request, 'Paginas\Grafo.html')

def grafo_data_api(request):
    # Esta vista genera y retorna los datos del grafo en formato JSON
    G = nx.Graph()
    G.add_nodes_from(['a', 'b', 'c'])
    G.add_edges_from([('a', 'b'), ('b', 'c')])

    nodes = [{'data': {'id': str(node)}} for node in G.nodes()]
    edges = [{'data': {'id': f'{source}{target}', 'source': str(source), 'target': str(target)}} for source, target in G.edges()]

    grafo_data = {
        'nodes': nodes,
        'edges': edges
    }

    return JsonResponse(grafo_data)
