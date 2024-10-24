# Esta es la historia de un fracaso...
import pandas as pd
#import graphviz as gv
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Image, display
from math import radians, sin, cos, sqrt, atan2
import re


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
        if distancia <= 80:
          G.add_edge(row1['nombre'], row2['nombre'], weight = distancia)

def dibujoGrafo():
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