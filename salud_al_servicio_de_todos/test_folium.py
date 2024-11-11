import folium
import pandas as pd
import IPython as ip
import networkx as nx
from pyvis.network import Network
import numpy as np
from math import radians, sin, cos, sqrt, atan2


min_lon, max_lon = -55, -95 # estos valores nos ayudan a restringir el movimiento del usuario en el mapa
min_lat, max_lat = -30, 20

# primer parametro es la longitud y latitud donde comienza la vista del mapa. Estos valores enfocan a Perú
# tiles es el diseño del mapa, Folium cuenta con varios diseños.
# zoom start es dónde comienza en zoom, min zoom es el zoom minimo y max zoom es el zoom máximo.
# max bounds restringe el mapa para que no se repita infinitamente.
m = folium.Map([-8.35, -74.6972], zoom_start=6, tiles= "CartoDB.Positron", min_zoom = 5, max_zoom=15,  max_bounds=True,
    min_lat=min_lat,max_lat=max_lat,
    min_lon=min_lon,max_lon=max_lon,)

f = folium.Figure(width=1000, height=500)

m.add_to(f) # agregamos el mapa m a la figura f para mantenerla en un recuadro creo

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distancia = R * c
    return round(distancia, 2) # Distancia aproximada a dos decimales


def optimizado_dibujar(num_nodos, cantidad, dibujar_aristas=False):
  df = pd.read_csv("data\out.csv", encoding='utf8', sep = ',', keep_default_na=False) # Lectura del .csv, datos separados por coma
  df = df.drop_duplicates(subset = 'nombre')

  for i in df.sample(n=cantidad).index:
     la = df['latitud'].iloc[i]
     if(la == ''): continue 
     lo = df['longitud'].iloc[i]
     ca = df['categoria'].iloc[i]
     no = df['nombre'].iloc[i]

     folium.Circle(
            location=[la, lo],
            radius=150,
            fill_opacity=1,
            fill_color="lightblue",
            popup= no + " -" + ca,
     ).add_to(m)
     
def dibujar_grafo(num_nodos, cantidad, dibujar_aristas=False):
  # se usa keep_default_na para que los valores vacios nos den un string vacio "" en vez de un "Nan"
  df = pd.read_csv("data\out.csv", encoding='utf8', sep = ',', keep_default_na=False) # Lectura del .csv, datos separados por coma
  
  df = df.drop_duplicates(subset = 'nombre')
  
  df = df.sample(n=cantidad)
  nodos = []

  for index, row in df.iterrows():

    # if("LIMA" not in row['diresa']): continue  # Tomamos los departamentos que tengan LIMA en el nombre
    if(row['latitud'] == "" or row['longitud'] == ""): continue # Algunos tienen la longitud o latitud vacios, no los queremos ver.
    nombre = row['nombre']
    # Creamos un circulo de Folium que representa a un nodo.
    folium.Circle(
        location=[row['latitud'], row['longitud']],
        radius=150,
        fill_opacity=1,
        fill_color="lightblue",
        popup= nombre + " -" + row['categoria'],
    ).add_to(m)
    nodos.append(row)

  
  if dibujar_aristas:
    max_ar = 4
    can_ar = 0
    for row1 in nodos:
        can_ar = 0
        for row2 in nodos:
            
            if row1["id_eess"] != row2["id_eess"]:
                
                la1 = np.float32(row1['latitud'])
                lo1 = np.float32(row1['longitud'])
                la2 = np.float32(row2['latitud'])
                lo2 = np.float32(row2['longitud'])
                distancia = haversine(la1, lo1, la2, lo2)
                if distancia <= 20:
                    can_ar += 1
                    folium.PolyLine(
                        locations=[
                        [la1, lo1], 
                        [la2, lo2],
                        ],
                        color="red",
                        weight=1,
                        popup= distancia,
                        
                    ).add_to(m)
        

csv_size = 16368 # cantidad de datos aproximado en el csv
cantidad = 1000 # maxima cantidad de Circles parece ser de 2060, por qué? no lo sé, maxima cantidad de Circle Markers?
dibujar_grafo(csv_size, cantidad, False)
# optimizado_dibujar(csv_size,cantidad, False)

m.save('templates/folium_map.html')