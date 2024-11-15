import pandas as pd
import graphviz as gv
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
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

    # Calcular las distancias
    distancias = R * c
    return distancias

# Hora de leer el archivo .xlsx
import re

# Ahora, a leer el archivo "TB_EESS-TB_EESS.csv",
# separando los datos de los hospitales por
# las comas en el csv

def mostrar_grafo_parcial(G, num_nodos):
  df = pd.read_csv('TB_EESS - TB_EESS.csv', sep = ',') # Lectura del .csv, datos separados por coma
  df = df.drop_duplicates(subset = 'nombre').head(num_nodos)

  for index, row in df.iterrows():
    G.add_node(row['nombre'], lat = row['latitud'], lon = row['longitud'])

  for i, row1 in df.iterrows():
    for j, row2 in df.iterrows():
      if i != j:
        distancia = haversine(row1['latitud'], row1['longitud'], row2['latitud'], row2['longitud'])
        if distancia <= 80 and distancia > 0:
          G.add_edge(row1['nombre'], row2['nombre'], weight = distancia)


# Dibujando el novo grafo
G = nx.Graph()
# Mostrar el grafo parcial
num_nodos = int(input("Número de nodos: "))

mostrar_grafo_parcial(G, num_nodos)

pos = nx.spring_layout(G, k = 2.0, scale = 2)
fig, ax = plt.subplots(figsize = (20, 20)) # Agrandar las dimensiones
nx.draw(G, pos, with_labels = True, ax = ax, node_color = "lightblue", node_size = 300, font_size = 8)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels = labels, rotate = False)
plt.show()


# ----------------------------------------------------------------------------------
# Dijkstra 

# Encontrar solo los nodos más cercanos a uno especificado
# Primero, el hospital más cercano a un nodo especificado.
# La función encontrar_nodos_cercanos(...) debe devolver
# el nodo (hospital y su nombre) y la distancia entre ellos.

# Ahora, realizaremos una función en la cual
# se ingrese el nombre de un hospital (nodo)
# y debe de obtenerse, como Output,
# el nodo más cercano, mediante Dijkstra.
import heapq as hp
import math

# Ahora, mostrar el grafo de un nodo específico (nombre tipeado de hospital)
def grafo_de_hospital(G, hospital):
  G_hospital = nx.Graph()
  G_hospital.add_node(hospital)

  for nodo in G.neighbors(hospital):
    G_hospital.add_edge(hospital, nodo, weight = G[hospital][nodo]['weight'])

  return G_hospital

def dijkstra_hospital(G, start_node):
  node_to_index = {node: i for i, node in enumerate(G.nodes())}
  index_to_node = {i: node for node, i in node_to_index.items()}
  n = len(G)

  visited = [False]*n
  path = [-1]*n
  cost = [math.inf]*n # Se inicializa en número infinitos

  start_index = node_to_index[start_node]
  cost[start_index] = 0
  # Creando cola pqueue
  pqueue = [(0, start_index)]

  while pqueue:
    g, u = hp.heappop(pqueue)

    if not visited[u]:
      visited[u] = True # Se marca como vértice visitado

      for neighbor in G.neighbors(index_to_node[u]):
        v = node_to_index[neighbor]
        if not visited[v]:
          if G.has_edge(index_to_node[u], index_to_node[v]):
            weight = G[index_to_node[u]][index_to_node[v]]['weight']
            f = g + weight
            if f < cost[v]:
              cost[v] = f
              path[v] = u
              hp.heappush(pqueue, (f, v))

  path = {index_to_node[i]: index_to_node[path[i]] for i in range(n) if path[i] != -1}
  dist = {index_to_node[i]: cost[i] for i in range(n)}

  return path, dist

# Filtrar hospitales más cercanos (<= 80 km)
def filtrar_hospitales_cercanos(G, hospital):
  path, dist = dijkstra_hospital(G, hospital) # Dijkstra. Se obtienen el camino y la distancia total (en km)

  hospitales_cercanos = {node: distancia for node, distancia in dist.items()
  if distancia <= 80 and node != hospital} # Se filtran los hospitales más cercanos (menor igual a 80 km)
                                           # y se asegura que no se incluya a sí mismo.

  return hospitales_cercanos

# Filtrar el hospital más cercano
def hospital_mas_cercano(G, hospital):
  path, dist = dijkstra_hospital(G, hospital)

  # Validación. No se contará a sí mismo.
  distancias_validas = {node: distancia for node, distancia in dist.items() if node != hospital}

  min_dist = min(distancias_validas.values())
  min_dist_node = [node for node, dist in dist.items() if dist == min_dist][0]
  # Se devuelve, también, el hospital más cercano en cuanto a distancia se refiere (en km).

  return min_dist_node, min_dist

# Comprobemos el código  del grafo del hospital
hospital = input("Hospital: ")

G_hos = grafo_de_hospital(G, hospital)

pos = nx.spring_layout(G_hos, k = 2.0, scale = 2)
fig, ax = plt.subplots(figsize = (20, 20)) # Agrandar las dimensiones
nx.draw(G_hos, pos, with_labels = True, ax = ax, node_color = "lightblue", node_size = 300, font_size = 8)
labels = nx.get_edge_attributes(G_hos, 'weight')
nx.draw_networkx_edge_labels(G_hos, pos, edge_labels = labels, rotate = False)
plt.show()

# Comprobando el código de hospitales cercanos
print()
hospitales_cercanos = filtrar_hospitales_cercanos(G_hos, hospital)
print(f"Hospitales cercanos: {hospitales_cercanos}")

# Comprobando el código de Dijkstra
print()
min_dist_node, min_dist = hospital_mas_cercano(G_hos, hospital)
print(f"Hospital más cercano: {min_dist_node}")
print(f"Distancia: {min_dist} km")

# -----------------------------------------------------------------------------------------------------
# Buscar por departamento

# Buscar nodos (hospitales) por departamento
# y otras características adicionales

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
  
# ------------------------------------------------------------------------------------------------------------------
# Buscar por categoría

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

# ---------------------------------------------------------------------------------------------------------------
# Dijkstra con dos centros ingresados

# Búsqueda en grafo
# Pensemos en otro...
# Dijkstra, con dos puntos ingresados (hospitales)
import heapq as hp
import math

def grafo_de_hospital(G, hospital):
  G_hospital = nx.Graph()
  G_hospital.add_node(hospital)

  for nodo in G.neighbors(hospital):
    G_hospital.add_edge(hospital, nodo, weight = G[hospital][nodo]['weight'])

  return G_hospital

def dijkstra_dos_puntos(G, start_node, end_node):
  node_to_index = {node: i for i, node in enumerate(G.nodes())}
  index_to_node = {i: node for node, i in node_to_index.items()}
  n = len(G)

  visited = [False]*n
  path = [-1]*n
  cost = [math.inf]*n # Se inicializa en número infinitos

  start_index = node_to_index[start_node]
  cost[start_index] = 0
  # Creando cola pqueue
  pqueue = [(0, start_index)]

  while pqueue:
    g, u = hp.heappop(pqueue)

    if u == end_node: # Si se llega al nodo destino, sale del ciclo while
      break

    if not visited[u]:
      visited[u] = True # Se marca como vértice visitado

      for neighbor in G.neighbors(index_to_node[u]):
        v = node_to_index[neighbor]
        if not visited[v]:
          if G.has_edge(index_to_node[u], index_to_node[v]):
            weight = G[index_to_node[u]][index_to_node[v]]['weight']
            f = g + weight
            if f < cost[v]:
              cost[v] = f
              path[v] = u
              hp.heappush(pqueue, (f, v))

    ruta = [] # Ruta para reconstruir el camino del nodo inicio al final
    # Crear grafo
    G_camino = nx.Graph()
    end_index = node_to_index[end_node]

    if cost[end_index] < math.inf:
      current_node = end_index
      while current_node != -1:
        ruta.append(index_to_node[current_node])
        current_node = path[current_node]
      ruta.reverse()

    # Agregar los nodos (dentro de camino)
    # para crear grafo del camino más cortos entre nodos
    for i in range(len(ruta) - 1):
      G_camino.add_edge(ruta[i], ruta[i + 1], weight = G[ruta[i]][ruta[i + 1]]['weight'])


  return ruta, cost[end_index], G_camino

# Comprobando el código
hospital1 = input("Hospital 1: ")
hospital2 = input("Hospital 2: ")

camino, distancia, G_camino = dijkstra_dos_puntos(G, hospital1, hospital2)
print(f"Camino: {camino}")
print(f"Distancia: {distancia} km")

# Ahora, mostremos el grafo de los nodos usados
pos = nx.spring_layout(G_camino, k = 2.0, scale = 2)
fig, ax = plt.subplots(figsize = (20, 20)) # Agrandar las dimensiones
nx.draw(G_camino, pos, with_labels = True, ax = ax, node_color = "green", node_size = 300, font_size = 8)
labels = nx.get_edge_attributes(G_camino, 'weight')
nx.draw_networkx_edge_labels(G_camino, pos, edge_labels = labels, rotate = False)
plt.show()
# Ejemplo de prueba
#Hospital 1: HOSPITAL IQUITOS "CESAR GARAYAR GARCÍA"
#Hospital 2: HOSPITAL REGIONAL DE LORETO "FELIPE SANTIAGO ARRIOLA IGLESIAS"