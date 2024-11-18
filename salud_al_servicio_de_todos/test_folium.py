import folium
import folium.map
import pandas as pd
import time
import numpy as np
import networkx as nx
import heapq as hp
from math import radians, sin, cos, sqrt, atan2, inf

# lat - long
dep_Coords = {"LIMA": (-11.9856,-76.6461), "AMAZONAS": (-5.0362,-78.0084), 
              "AREQUIPA": (-15.9666,-72.3669), "CUSCO": (-12.8439,-72.4164),
              "ICA":(-14.5251,-75.5090), "LORETO": (-5.1402,-74.9982), "CALLAO":(-11.9641,-77.1151),
              "CAJAMARCA":(-6.2880, -78.8214), "PIURA": (-5.0526, -80.3156), "ANCASH":(-9.6305,-77.4976),
              "TACNA":(-17.6493,-70.3015), "APURIMAC":( -14.0860, -72.9822), "LAMBAYEQUE":( -6.3508, -79.9750), "SAN MARTIN": ( -7.0464,-76.8246),
              "UCAYALI": ( -9.0316, -73.5123), "MOQUEGUA":(-16.8781,-70.8838), "PUNO": (-15.0138, -69.9747),
              "MADE DE DIOS": (-12.0017, -70.2411), "JUNIN" : ( -11.5042, -74.9982), "PASCO":(-10.4973, -75.2481),
              "HUANUCO": (-9.5520, -75.2481), "LA LIBERTAD": ( -8.0266, -78.4726), "TUMBES":(-3.8149, -80.5408),
              "HUANCAVELICA": (-12.9805, -75.0229), "AYACUCHO":(-14.0380, -73.9819)}

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

def create_Dataframe(cantidad):
    df = pd.read_csv("data\out.csv", encoding='utf8', sep = ',').head(cantidad) # Lectura del .csv, datos separados por coma
    return df

def apply_(row, df,graph,mapa, dist, max_ar):
  la = row['latitud']
  lo = row['longitud']
  ca = row['categoria']
  no = row['nombre']

  graph.add_node(row['nombre'])
  # Agregando aristas al grafo G_dep, si la distancia entre hospitales es <= 80 km

  folium.Circle(
        location=[la, lo],
        radius=150,
        fill_opacity=1,
        fill_color="lightblue",
        popup= no + " -" + ca,
  ).add_to(mapa)

  ar = 0
  for j in range(len(df)):
    if ar >= max_ar: break
    if row["id_eess"] != df["id_eess"].iloc[j]: 
      la1 = np.float32(la)
      lo1 = np.float32(lo)
      la2 = np.float32(df['latitud'].iloc[j])
      lo2 = np.float32(df['longitud'].iloc[j])
      distancia = haversine(la1, lo1, la2, lo2)
      if distancia <= dist:
        ar += 1
        graph.add_edge(no, df['nombre'].iloc[j], weight = distancia)
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

def folium_from_nx(row, df, graph, mapa, dist):
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

    nodos = list(graph.nodes)
    for j in range(len(df)):
      if df['nombre'].iloc[j] not in nodos: continue
      if row["id_eess"] != df["id_eess"].iloc[j]: 
        la1 = np.float32(la)
        lo1 = np.float32(lo)
        la2 = np.float32(df['latitud'].iloc[j])
        lo2 = np.float32(df['longitud'].iloc[j])
        distancia = haversine(la1, lo1, la2, lo2)
        if distancia <= dist:
          folium.PolyLine(
              locations=[
              [la1, lo1], 
              [la2, lo2],],
              color="red",
              weight=1,
              popup= distancia,
          ).add_to(mapa)

def folium_from_dijkstra(row, df, graph, mapa, costo):
  nodos = list(graph.nodes)
  for a, i in enumerate(nodos):
    if(i != row['nombre']): continue
    la = row['latitud']
    lo = row['longitud']
    ca = row['categoria']
    no = row['nombre']

    folium.Circle(
      location=[la, lo],
      radius=170,
      fill_opacity=1,
      fill_color="lightblue",
      popup= no + " -" + ca,
    ).add_to(mapa)

    if(a > 0): # si podemos retroceder en la lista nodos, buscamos el nodo anterior en el df
      for j in range(len(df)):
        if df['nombre'].iloc[j] != nodos[a - 1]: continue

        la1 = np.float32(la)
        lo1 = np.float32(lo)
        la2 = np.float32(df['latitud'].iloc[j])
        lo2 = np.float32(df['longitud'].iloc[j])
        distancia = haversine(la1, lo1, la2, lo2)
        folium.PolyLine(
            locations=[
            [la1, lo1], 
            [la2, lo2],],
            color="red",
            weight=4,
            popup= distancia,
        ).add_to(mapa)
    else:
      folium.Marker(
      location= (la + 1, lo -1),
      popup= "camino más corto es de " + str(costo) + "km.",
      tooltip= "Camino más corto"
    ).add_to(mapa)

def apply_networkx(row, df, graph, dist):
  # Búsqueda de hospitales segun departamento
  graph.add_node(row['nombre'])
  la = row['latitud']
  lo = row['longitud']
  no = row['nombre']
  # Agregando aristas al grafo G_dep, si la distancia entre hospitales es <= 80 km
  for j in range(len(df)):
    if row["id_eess"] == df["id_eess"].iloc[j]: continue
    
    distancia = haversine(la, lo, df['latitud'].iloc[j], df['longitud'].iloc[j])
    if distancia <= dist:
      graph.add_edge(no, df['nombre'].iloc[j], weight = distancia)

def apply_df_dep(row, df, departamento):
  if departamento in row['diresa']:
    i = len(df.index)
    df.loc[i] = row

def buscar_hospital_por_categoria(categoria):
  df_cat = df[df['categoria'] == categoria]
  print("busqueda por categoria....")
  graph_cat = nx.Graph()
  ma = folium.Map([-8.35, -74.6972], zoom_start=6, tiles= "CartoDB.Positron", min_zoom = 5, max_zoom=15,  max_bounds=True,
    min_lat=min_lat,max_lat=max_lat,
    min_lon=min_lon,max_lon=max_lon,)
  
  print("empezo el sample...")
  df_cat = df_cat.sample(n=1500 if len(df_cat) >= 1500 else len(df_cat))
  print("empezo networkx..")
  df_cat.apply(apply_, axis=1, args=(df_cat, graph_cat, ma, 10, 2))
  print("acabo networkx")
  print("acabo folium")
  ma.save('templates/folium_map.html')
  print("finish!", graph_cat.number_of_nodes())

def buscar_hospital_por_departamento(departamento):
  print("busqueda por departamento....")
  df_dep = pd.DataFrame(columns=df.columns)
  departamento = departamento.upper()
  df.apply(apply_df_dep, axis=1, args=(df_dep, departamento))
  df_dep = df_dep.sample(n=1500 if len(df_dep) >=1500 else len(df_dep))
  graph_cat = nx.Graph()
  #[-8.35, -74.6972]
  ma = folium.Map(dep_Coords[departamento], zoom_start=8, tiles= "CartoDB.Positron", min_zoom = 5, max_zoom=15,  max_bounds=True,
    min_lat=min_lat,max_lat=max_lat,
    min_lon=min_lon,max_lon=max_lon,)
  
  dist = 2 if departamento == 'LIMA' else 10
  print("empezo networkx y folium")

  df_dep.apply(apply_, axis=1, args=(df_dep, graph_cat, ma, dist, 3))

  print("acabo networkx y folium")

  ma.save('templates/folium_map.html')
  print("finish! ", graph_cat.number_of_nodes())
  
def buscar_doble(departamento, categoria):
  df_dep = pd.DataFrame(columns=df.columns)
  departamento = departamento.upper()
  df.apply(apply_df_dep, axis=1, args=(df_dep, departamento))
  # df_dep = df_dep.sample(n=1500 if len(df_dep) >=1500 else len(df_dep))

  df_cat = df_dep[df_dep['categoria'] == categoria]
  df_cat = df_cat.sample(n=1500 if len(df_cat) >=1500 else len(df_cat))

  graph_cat = nx.Graph()

  ma = folium.Map([-8.35, -74.6972], zoom_start=6, tiles= "CartoDB.Positron", min_zoom = 5, max_zoom=15,  max_bounds=True,
    min_lat=min_lat,max_lat=max_lat,
    min_lon=min_lon,max_lon=max_lon,)

  print("empezo networkx")
  dist = 2 if departamento == 'LIMA' else 10
  df_cat.apply(apply_, axis=1, args=(df_cat, graph_cat, ma, dist, 3)) # pasar grafo a networkx
  print("acabo networkx")
  
  print("acabo folium")
  ma.save('templates/folium_map.html')
  print("finish! ", graph_cat.number_of_nodes())
  return graph_cat, df_cat

def dijkstra(start, end):
  # print(start, start.strip())
  # print(start, start.replace(" ", ""))
  dijkstra_dos_puntos(graph, start.strip(), end.strip())

def dijkstra_dos_puntos(G, start_node, end_node):

  node_to_index = {node.strip(): i for i, node in enumerate(G.nodes())}
  index_to_node = {i: node.strip() for node, i in node_to_index.items()}
  n = len(G)

  visited = [False]*n
  path = [-1]*n
  cost = [inf]*n # Se inicializa en número infinitos

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

    if cost[end_index] < inf:
      current_node = end_index
      while current_node != -1:
        ruta.append(index_to_node[current_node])
        current_node = path[current_node]
      ruta.reverse()

    # Agregar los nodos (dentro de camino)
    # para crear grafo del camino más cortos entre nodos
    for i in range(len(ruta) - 1):
      G_camino.add_edge(ruta[i], ruta[i + 1], weight = G[ruta[i]][ruta[i + 1]]['weight'])

  ma = folium.Map([-8.35, -74.6972], zoom_start=6, tiles= "CartoDB.Positron", min_zoom = 5, max_zoom=15,  max_bounds=True,
    min_lat=min_lat,max_lat=max_lat,
    min_lon=min_lon,max_lon=max_lon,)
  

  dij_df.apply(folium_from_dijkstra, axis=1, args=(dij_df, G_camino, ma, cost[end_index]))
  ma.save('templates/folium_map.html')

csv_size = 16368 # cantidad de datos aproximado en el csv
cantidad = 1500 # maxima cantidad de Circles parece ser de 2060, por qué? no lo sé, maxima cantidad de Circle Markers?
# dibujar_grafo(csv_size, cantidad, False)

df = create_Dataframe(csv_size)# creamos dataframe

print("SE CREO EL DATASET....")

graph = nx.Graph()
dij_df = pd.DataFrame()

def start_map():
  af = df.sample(n = 1500)
  af.apply(apply_dibujar, axis = 1, args=(af, False))
  m.add_child(folium.LatLngPopup())
  m.save('templates/folium_map.html')