# Esta es el comienzo de un fracaso
# Únanse al baile, de los que sobran
# Nadie nos quiso ayudar, de verdad
# Viva el Che y los Rolling Stones
# Number 9
# Anarquista, hessiano y turbomano
# Abajo Fidel
# XDdxxdDX
# AIDOIJiomdhmienfij036#"°+[kJUHA
# Buscar nodos (hospitales) por departamento
# y otras características adicionales
from IPython.display import Image, display
from math import radians, sin, cos, sqrt, atan2

# Radio de la Tierra en kilómetros
R = 6371.0

# Fórmula de Haversine, conversor de latitud y longitud a distancias (en km)
def haversine(lat1, lon1, lat2, lon2):
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distancia = R * c
    return round(distancia, 2) # Distancia aproximada a dos decimales


import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

def buscar_hospital_por_departamento(G, dep):
  df = pd.read_csv('TB_EESS - TB_EESS.csv', sep = ',')
  df_dep = df[df['diresa'].str.lower() == dep.lower()]

  G_dep = nx.Graph()

  # Agregando nodos al grafo G_dep
  for index, row in df_dep.iterrows():
    G_dep.add_node(row['nombre'], lat = row['latitud'], lon = row['longitud'])

  # Agregando aristas al grafo G_dep, si la distancia entre hospitales es <= 80 km
  for i, row1 in df_dep.iterrows():
    for j, row2 in df_dep.iterrows():
      if i != j:
        distancia = haversine(row1['latitud'], row1['longitud'], row2['latitud'], row2['longitud'])
        if distancia <= 80:
          G_dep.add_edge(row1['nombre'], row2['nombre'], weight = distancia)

  return G_dep # Se devuelve al grafo con los hospitales del departamento ingresado

# Probando el código
dep = input("Ingrese nombre del departamento en Perú: ")
G_dep = buscar_hospital_por_departamento(G, dep)

# Dibujando el grafo
pos = nx.spring_layout(G_dep, k = 2.0, scale = 2)
fig, ax = plt.subplots(figsize=(20, 20))
nx.draw(G_dep, pos, with_labels = True, ax = ax, node_color = "yellow", node_size = 300, font_size = 8)
labels = nx.get_edge_attributes(G_dep, 'weight')
nx.draw_networkx_edge_labels(G_dep, pos, edge_labels = labels, rotate = False)
plt.show()

# Ahora, veamos qué
# Buscar hospitales por categoría
# Implementación:
def buscar_hospital_por_categoria(G, cat):
  df = pd.read_csv('TB_EESS - TB_EESS.csv', sep = ',') # Se lee el .csv
  df_cat = df[df['categoria'].str.lower() == cat.lower()] # Búsqueda de hospitales con categoría coincidente a la ingresada.

  G_cat = nx.Graph()

  # Agregando nodos al grafo G_dep
  for index, row in df_cat.iterrows():
    G_dep.add_node(row['nombre'], lat = row['latitud'], lon = row['longitud'])

  # Agregando aristas al grafo G_dep, si la distancia entre hospitales es <= 80 km
  for i, row1 in df_cat.iterrows():
    for j, row2 in df_cat.iterrows():
      if i != j:
        distancia = haversine(row1['latitud'], row1['longitud'], row2['latitud'], row2['longitud'])
        if distancia <= 80:
          G_cat.add_edge(row1['nombre'], row2['nombre'], weight = distancia)

  return G_cat # Se devuelve al grafo con los hospitales del departamento ingresado

# Siguiente parte del código:
cat = input("Ingrese categoría: ")
G_cat = buscar_hospital_por_categoria(G, cat)

# Dibujando el grafo
pos = nx.spring_layout(G_cat, k = 2.0, scale = 2)
fig, ax = plt.subplots(figsize=(20, 20))
nx.draw(G_cat, pos, with_labels = True, ax = ax, node_color = "green", node_size = 300, font_size = 8)
labels = nx.get_edge_attributes(G_cat, 'weight')
nx.draw_networkx_edge_labels(G_cat, pos, edge_labels = labels, rotate = False)
plt.show()