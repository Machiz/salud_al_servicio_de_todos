# **Salud al Servicio de Todos**

Este proyecto es una aplicación web desarrollada con **Django** y **JavaScript** para visualizar gráficos y datos relacionados con el sistema de salud. Utiliza bibliotecas como **Folium** para la visualización de mapas interactivos y **Cytoscape.js** para la visualización de redes. Además, se gestionan datos a partir de un archivo CSV con información sobre ubicaciones y otras propiedades de puntos de interés.

### **Guía de Ejecución desde VSCode**

Para facilitar el proceso de configuración del entorno de desarrollo y la instalación de las dependencias, hemos configurado **tareas automatizadas en VSCode**. Solo necesitas ejecutar una tarea para crear un entorno virtual y asegurarte de que todas las dependencias se instalen correctamente.

1. **Abre el proyecto en VSCode**:
   Si aún no lo has hecho, abre **VSCode** y carga el proyecto mediante `File > Open Folder...`.

2. **Verifica que las tareas estén configuradas**:
   Asegúrate de que el archivo `tasks.json` se encuentre en el directorio `.vscode`. Si no está presente, crea este archivo siguiendo las instrucciones en la sección de **Estructura del Proyecto**.

3. **Ejecutar la tarea para crear el entorno virtual y las dependencias**:
   
   En VSCode, puedes ejecutar una tarea a través del panel de comandos. Para ello, sigue estos pasos:
   
   - Abre la **Paleta de Comandos** en VSCode con `Ctrl + Shift + P`.
   - Escribe **Run Task** y selecciona **"Crear entorno virtual e instalar dependencias"**.
   
   Este comando ejecutará una serie de acciones:
   - Verificará si el entorno virtual `.venv` ya existe.
   - Si no existe, creará el entorno virtual y luego instalará las dependencias desde el archivo `requirements.txt`.
   - Si el entorno virtual ya está creado, solo instalará las dependencias.

4. **Activar el entorno virtual**:
   Después de que el entorno virtual haya sido creado y las dependencias se hayan instalado, asegúrate de activar el entorno virtual desde la terminal de VSCode. Para esto, puedes usar el siguiente comando:
   
   - En Windows:  
     ```bash
     .\.venv\Scripts\activate
     ```
   
   - En macOS/Linux:  
     ```bash
     source .venv/bin/activate
     ```

5. **Iniciar el servidor Django**:
   Ahora, puedes iniciar el servidor de desarrollo de Django. En la terminal de VSCode, ejecuta el siguiente comando:
   ```bash
   python manage.py runserver
   ```

6. **Accede a la aplicación**:
   Abre tu navegador y navega a `http://127.0.0.1:8000/` para ver la aplicación en funcionamiento.

---

### **Pasos Alternativos (Manual)**

Si prefieres realizar la configuración manualmente, sigue estos pasos:

1. **Clonar el repositorio**:

   Si aún no has clonado el repositorio, abre una terminal y ejecuta:
   ```bash
   git clone https://github.com/tu_usuario/salud_al_servicio_de_todos.git
   cd salud_al_servicio_de_todos
   ```

2. **Configurar el entorno virtual** (opcional pero recomendado):
   - En Windows:
     ```bash
     python -m venv .venv
     .\.venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```

3. **Instalar las dependencias**:
   Ejecuta el siguiente comando para instalar todas las dependencias desde el archivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Migrar la base de datos** (si es necesario):
   Si tu proyecto requiere migración de base de datos, ejecuta:
   ```bash
   python manage.py migrate
   ```

5. **Iniciar el servidor de desarrollo**:
   Ejecuta el siguiente comando para iniciar el servidor:
   ```bash
   python manage.py runserver
   ```

6. **Acceder a la aplicación**:
   Abre tu navegador y navega a `http://127.0.0.1:8000/` para ver la aplicación en funcionamiento.

---
### **Estructura del Proyecto**

A continuación se describe la estructura de carpetas y archivos, junto con un comentario sobre su propósito.

```
D:.
│
│   README.md                  # Página HTML relacionada con Folium
│   manage.py                        # Script de administración de Django
│   .gitignore                    # Archivos y carpetas a ignorar en Git
│   requeriments.txt              # Archivo con las dependencias del proyecto
│
├───.vscode
│       extensions.json          # Configuración específica de extensiones para VSCode
│       settings.json            # Configuración local de VSCode
│
├───data
│       data.csv                 # Archivo CSV con datos para la visualización
│
├───export
│       folium_map.html          # Mapa generado con Folium exportado a HTML
│
├───lib
│   ├───bindings
│   │       utils.js             # Funciones de utilidad personalizadas
│   │
│   ├───tom-select
│   │       tom-select.complete.min.js  # Archivo JavaScript de la librería Tom Select
│   │       tom-select.css        # Estilos CSS para la librería Tom Select
│   │
│   └───vis-9.1.2
│           vis-network.css      # Estilos CSS de la librería vis-network
│           vis-network.min.js   # Archivo JavaScript de la librería vis-network
│
├───salud_al_servicio_de_todos
│       asgi.py                   # Configuración para servidor ASGI
│       grafo.py                  # Lógica para la creación y manipulación de grafos
│       settings.py               # Configuración general de Django
│       test_folium.py            # Pruebas unitarias relacionadas con Folium
│       urls.py                   # Rutas del proyecto Django
│       views.py                  # Vistas de la aplicación web
│       wsgi.py                   # Configuración para servidor WSGI
│
├───static
│   ├───css
│   │       styles.css           # Estilos CSS adicionales para la interfaz
│   │
│   └───js
│           interface.js         # Lógica JavaScript para la interfaz web
│
└───templates
        Index.html               # Página principal de la interfaz
        nx.html                   # Página de visualización del grafo generado
```

---

### **Descripción de los Archivos y Carpetas**

#### **Archivos en la raíz del proyecto:**

- **`README.md`**:  
  Este archivo contiene información general sobre el proyecto. Aquí se debe incluir una descripción del proyecto, instrucciones de instalación, cómo ejecutar el proyecto, requisitos del sistema y cualquier otro detalle relevante.

- **`manage.py`**:  
  Es el archivo principal de Django para interactuar con el proyecto. A través de este archivo, puedes ejecutar comandos como `python manage.py runserver` para iniciar el servidor o `python manage.py migrate` para realizar migraciones de base de datos.

- **`.gitignore`**:  
  Este archivo contiene una lista de archivos y directorios que deben ser ignorados por Git. Ejemplos comunes son archivos de configuración específicos de entornos, directorios de caché o el entorno virtual (`.env`).

- **`requirements.txt`**:  
  Contiene una lista de todas las dependencias del proyecto. Puedes instalar estas dependencias utilizando el comando `pip install -r requirements.txt` en un entorno virtual.

#### **Directorios en el proyecto:**

- **`.vscode/`**:  
  Contiene configuraciones específicas de Visual Studio Code para el proyecto, como la configuración de extensiones y preferencias del editor.

  - **`extensions.json`**:  
    Lista las extensiones recomendadas para trabajar en este proyecto con VSCode.
  
  - **`settings.json`**:  
    Configuraciones locales de VSCode para este proyecto (como la configuración de formato de código, reglas de estilo, etc.).

- **`data/`**:  
  Contiene el archivo **`data.csv`**, que es la fuente de datos del proyecto. Este archivo debe contener datos relacionados con la visualización de los grafos (por ejemplo, coordenadas geográficas y nombres de los nodos).

- **`export/`**:  
  Este directorio almacena el archivo **`folium_map.html`**, generado por la librería **Folium**. Este archivo contiene un mapa interactivo exportado a HTML que se puede abrir en cualquier navegador web.

- **`lib/`**:  
  Aquí se encuentran las bibliotecas de JavaScript que se utilizan para la visualización de datos, como **Tom Select** para mejorar los formularios y **vis-network** para la visualización de redes.

  - **`bindings/`**:  
    Contiene el archivo **`utils.js`**, que parece ser un archivo de utilidades JavaScript con funciones personalizadas que pueden usarse a lo largo del proyecto.

  - **`tom-select/`**:  
    Contiene los archivos de la librería **Tom Select**, una herramienta para crear listas desplegables mejoradas y dinámicas en la interfaz web.

  - **`vis-9.1.2/`**:  
    Aquí se encuentran los archivos de la librería **vis-network**, que se utiliza para la visualización de redes o grafos interactivos en el frontend. El archivo **`vis-network.min.js`** es el script principal y **`vis-network.css`** es el archivo de estilo.

- **`salud_al_servicio_de_todos/`**:  
  Este es el directorio principal de la aplicación Django. Contiene la configuración y las vistas de la aplicación.

  - **`asgi.py`**:  
    Configura el servidor ASGI para proyectos Django. Si estás utilizando **Django Channels** o servicios en tiempo real, este archivo es relevante.

  - **`grafo.py`**:  
    Este archivo contiene la lógica de Python relacionada con la creación y manipulación de los grafos. Aquí se pueden definir las funciones para procesar los datos del CSV, construir los grafos y exportarlos.

  - **`settings.py`**:  
    Contiene toda la configuración de Django, incluyendo la base de datos, la seguridad, las rutas estáticas, aplicaciones instaladas y más.

  - **`test_folium.py`**:  
    Archivo de pruebas que contiene pruebas unitarias o de integración para las funciones relacionadas con **Folium**.

  - **`urls.py`**:  
    Define las rutas de la aplicación Django. Aquí se mapea cada URL a una vista específica.

  - **`views.py`**:  
    Define las vistas de Django que se encargan de procesar las solicitudes HTTP y devolver las respuestas correspondientes, generalmente en formato HTML, JSON o redirecciones.

  - **`wsgi.py`**:  
    Configuración para el servidor WSGI de Django. Usado principalmente para despliegue en producción.

- **`static/`**:  
  Contiene archivos estáticos como CSS y JavaScript que se sirven directamente a los clientes (navegadores).

  - **`css/`**:  
    Contiene el archivo **`styles.css`**, que define los estilos CSS adicionales utilizados en la interfaz de la aplicación.

  - **`js/`**:  
    Contiene el archivo **`interface.js`**, que maneja la lógica JavaScript para la interfaz de usuario (interactividad, visualización de datos, etc.).

- **`templates/`**:  
  Este directorio contiene los archivos HTML de la interfaz web. Django los utiliza para renderizar las vistas en el navegador.

  - **`Index.html`**:  
    Página principal que probablemente sirva como punto de entrada a la aplicación.

  - **`nx.html`**:  
    Este archivo parece estar relacionado con la visualización de un grafo, probablemente utilizando una librería como **Cytoscape.js** o **vis-network**.
