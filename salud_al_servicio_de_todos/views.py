# grafo_app/views.py
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
#from . import djikstra

@csrf_exempt
def main_view(request):
    # con esto se validan los parametros
    if request.method == 'POST':
        # Process the form data
        salud = request.POST.get('csalud')
        saludf = request.POST.get('csaludf')
        provincia = request.POST.get('provincia')
        categoria = request.POST.get('categoria')

        # You can do something with the data here, like saving it to the database

        # Redirect to another page after processing
        return HttpResponse("Do something")  # Redirect to the URL named 'another_page'
    # Esta vista renderiza la plantilla HTML para mostrar el grafo
    return render(request, 'index.html')
def fol_view(request):
    # Esta vista renderiza la plantilla HTML para mostrar el grafo
    return render(request, 'folium_map.html')
#funcion para el formulario parametrado
@csrf_exempt
def formulario_procesado(request):
    return render(request, 'folium_map.html')
    