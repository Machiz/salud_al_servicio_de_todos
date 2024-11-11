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
import networkx as nx
import matplotlib.pyplot as plt

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

# Dijkstra para dos centros específicos
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