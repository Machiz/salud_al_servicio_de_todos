# grafo_app/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from . import grafo

def main_view(request):
    # Esta vista renderiza la plantilla HTML para mostrar el grafo
    return render(request, 'index.html')
def fol_view(request):
    # Esta vista renderiza la plantilla HTML para mostrar el grafo
    return render(request, 'folium_map.html')
def procesar_formulario(request):
    if request.method == 'POST':
        # Recibir datos del formulario
        search_value_range = request.POST.get('search_value_range')
        departamento = request.POST.get('departamento')
        categoria = request.POST.get('categoria')
        csalud = request.POST.get('csalud')
        csaludf = request.POST.get('csaludf')
        
        # Procesar los datos según la lógica de la aplicación
        # (Ejemplo: almacenar en la base de datos, realizar cálculos, etc.)

        # Retornar una respuesta (puede ser una redirección o renderizar una nueva página)
        return HttpResponse(f"Datos recibidos: Rango de búsqueda: {search_value_range}, "
                            f"Departamento: {departamento}, Categoría: {categoria}, "
                            f"Centro de Salud Inicial: {csalud}, Centro de Salud Final: {csaludf}")

    return render(request, 'grafo.html')