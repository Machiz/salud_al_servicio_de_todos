import folium
import pandas as pd
import networkx as nx
from pyvis.network import Network

path_csv = "data/data.csv"
export_folium = "export/folium_map.html"

m = folium.Map([-8.35, -74.6972], zoom_start=6, tiles= "CartoDB.Positron",min_zoom = 5, max_zoom=13,  max_bounds=True)
f = folium.Figure(width=1000, height=500)
m.add_to(f)

def dibujar_grafo(num_nodos):
  df = pd.read_csv(path_csv, encoding='utf8', sep = ',', keep_default_na=False) # Lectura del .csv, datos separados por coma
  df = df.drop_duplicates(subset = 'nombre').head(num_nodos)
  radius = 200
  for index, row in df.iterrows():
    if(row['latitud'] == "" or row['longitud'] == ""): continue
    folium.Circle(
        location=[row['latitud'], row['longitud']],
        radius=radius,
        color="black",
        weight=1,
        fill_opacity=0.6,
        opacity=1,
        fill_color="green",
        fill=False,  # gets overridden by fill_color
        popup="{} meters".format(radius),
        tooltip= row['nombre'],
    ).add_to(m)

def mostrar_grafo_parcial(G, num_nodos):
  df = pd.read_csv(path_csv, sep = ',') # Lectura del .csv, datos separados por coma
  df = df.drop_duplicates(subset = 'nombre').head(num_nodos)

  for index, row in df.iterrows():
    G.add_node(str(row['nombre']), lat = row['latitud'], lon = row['longitud'])

# G = nx.Graph()
# mostrar_grafo_parcial(G, 20)
# nx.draw(G, with_labels = True)

# nt = Network('500px', '500px')
# nt.from_nx(G)
# nt.show('nx.html', notebook=False)


dibujar_grafo(2000)
m.save(export_folium)