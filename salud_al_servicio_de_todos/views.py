# grafo_app/views.py
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import test_folium
#from . import djikstra

@csrf_exempt
def main_view(request):
    # con esto se validan los parametros
    # Esta vista renderiza la plantilla HTML para mostrar el grafo
    test_folium.start_map()
    return render(request, 'index.html')
def fol_view(request):
    # Esta vista renderiza la plantilla HTML para mostrar el grafo
    return render(request, 'folium_map.html')
#funcion para el formulario parametrado
@csrf_exempt
def formulario_procesado(request):
    if request.method == 'POST':
        # Process the form data
        salud = request.POST.get('csalud')
        saludf = request.POST.get('csaludf')
        provincia = request.POST.get('departamento')
        categoria = request.POST.get('categoria')

        # You can do something with the data here, like saving it to the database
        if salud != '' and saludf != '':
            test_folium.dijkstra(salud, saludf)
        elif provincia != 'none' and categoria != 'none': 
            test_folium.graph, test_folium.dij_df = test_folium.buscar_doble(provincia, categoria)
        elif provincia != 'none':    
            test_folium.buscar_hospital_por_departamento(provincia)
        elif categoria != 'none':
            test_folium.buscar_hospital_por_categoria(categoria)
        
        # Redirect to another page after processing
        return render(request, 'folium_map.html')  # Redirect to the URL named 'another_page'
    return render(request, 'folium_map.html')
    