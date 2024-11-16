import folium
import folium.map
import pandas as pd
import time
import numpy as np
import networkx as nx
import heapq as hp
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
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distancia = 6371.0 * c
    return round(distancia, 2) # Distancia aproximada a dos decimales

def create_Dataframe():
    df = pd.read_csv("data\out.csv", encoding='utf8', sep = ',') # Lectura del .csv, datos separados por coma
    return df

def filtrar(departamento):
  mapa = folium.Map([-8.35, -74.6972], zoom_start=6, tiles= "CartoDB.Positron", min_zoom = 5, max_zoom=15,  max_bounds=True,
    min_lat=min_lat,max_lat=max_lat,
    min_lon=min_lon,max_lon=max_lon,)
  df.apply(apply_departamento, axis=1, args=(df,departamento, mapa))
  mapa.save('templates/folium_map.html')

def apply_departamento(row, df, departamento, mapa):
  if(departamento not in row['diresa']): return

  la = row['latitud']
  lo = row['longitud']
  ca = row['categoria']
  no = row['nombre']

  folium.Circle(
        location=[la, lo],
        radius=150,
        fill_opacity=1,
        fill_color="lightblue",
        popup= no + " -" + ca,
  ).add_to(mapa)

  for j in range(len(df)):
      if row["id_eess"] != df["id_eess"].iloc[j]: 
            la1 = np.float32(la)
            lo1 = np.float32(lo)
            la2 = np.float32(df['latitud'].iloc[j])
            lo2 = np.float32(df['longitud'].iloc[j])
            distancia = haversine(la1, lo1, la2, lo2)
            if distancia <= 20:
                folium.PolyLine(
                    locations=[
                    [la1, lo1], 
                    [la2, lo2],],
                    color="red",
                    weight=1,
                    popup= distancia,
                ).add_to(mapa)

def apply_dibujar(row, df, aristas = False):
  la = row['latitud']
  lo = row['longitud']
  ca = row['categoria']
  no = row['nombre']

  folium.Circle(
    location=[la, lo],
    radius=150,
    fill_opacity=1,
    fill_color="lightblue",
    popup= no + " -" + ca,
  ).add_to(m)

  if(aristas == False): return
  for j in range(len(df)):
    if row["id_eess"] != df["id_eess"].iloc[j]: 
      la1 = np.float32(la)
      lo1 = np.float32(lo)
      la2 = np.float32(df['latitud'].iloc[j])
      lo2 = np.float32(df['longitud'].iloc[j])
      distancia = haversine(la1, lo1, la2, lo2)
      if distancia <= 20:
          folium.PolyLine(
              locations=[
              [la1, lo1], 
              [la2, lo2],],
              color="red",
              weight=1,
              popup= distancia,
          ).add_to(m)

def create_networkx(row, df, graph):
  graph.add_node(row['nombre'])
  la = row['latitud']
  lo = row['longitud']
  for j in range(len(df)):
    if row["id_eess"] != df["id_eess"].iloc[j]: 
      la1 = np.float32(la)
      lo1 = np.float32(lo)
      la2 = np.float32(df['latitud'].iloc[j])
      lo2 = np.float32(df['longitud'].iloc[j])
      distancia = haversine(la1, lo1, la2, lo2)
      if distancia <= 20:
        graph.add_edge(row['nombre'], df['nombre'].iloc[j], weight= distancia)  

def folium_from_nx(row, df, graph, mapa):
  for i in list(graph.nodes):
    if(i != row['nombre']): continue
    la = row['latitud']
    lo = row['longitud']
    ca = row['categoria']
    no = row['nombre']

    folium.Circle(
      location=[la, lo],
      radius=150,
      fill_opacity=1,
      fill_color="lightblue",
      popup= no + " -" + ca,
    ).add_to(mapa)

    for j in range(len(df)):
      if row["id_eess"] != df["id_eess"].iloc[j]: 
        la1 = np.float32(la)
        lo1 = np.float32(lo)
        la2 = np.float32(df['latitud'].iloc[j])
        lo2 = np.float32(df['longitud'].iloc[j])
        distancia = haversine(la1, lo1, la2, lo2)
        if distancia <= 20:
          folium.PolyLine(
              locations=[
              [la1, lo1], 
              [la2, lo2],],
              color="red",
              weight=1,
              popup= distancia,
          ).add_to(mapa)

csv_size = 16368 # cantidad de datos aproximado en el csv
cantidad = 100 # maxima cantidad de Circles parece ser de 2060, por qué? no lo sé, maxima cantidad de Circle Markers?
# dibujar_grafo(csv_size, cantidad, False)

df = create_Dataframe()    # creamos dataframe
df = df.sample(n=cantidad) # elegir datos dispersos del dataframe

graph = nx.Graph()

df.apply(create_networkx, axis=1, args=(df, graph,)) # creamos grafo networkx
t = time.time()
df.apply(folium_from_nx, axis=1, args=(df, graph, m))
# df.apply(apply_dibujar, axis=1, args=(df,False))
print((time.time() - t) * 1000, "ms")
m.save('templates/folium_map.html')