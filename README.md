### Steam Game Recommendation System

Este proyecto se centra en el desarrollo de una API utilizando FastAPI para proporcionar funcionalidades relacionadas con la recomendación de videojuegos en la plataforma Steam. Implica tareas de transformación de datos, ingeniería de características, desarrollo de la API y despliegue en un servicio en la nube como Render.

#### Flujo General del Proyecto

1. **Ingeniería de Datos**:
   - Ingesta de datos desde diversas fuentes como archivos CSV, una API y técnicas de scrapping.
   - Tratamiento de datos para garantizar calidad y utilidad.
   - Carga y disponibilización de datos a través de una API para facilitar su acceso.

2. **Desarrollo del Modelo de Machine Learning**:
   - Análisis exploratorio de datos para comprender patrones y tendencias.
   - Experimentación con diferentes algoritmos y técnicas de modelado.
   - Desarrollo del modelo final para la recomendación de videojuegos.

3. **Implementación y Uso del Modelo**:
   - Integración del modelo en la aplicación o sistema para su uso efectivo.
   - Mantenimiento y actualización de la infraestructura del modelo según sea necesario.

#### Estructura de Querys para Construcción de los Endpoints

1. **Endpoint para obtener al usuario con más horas jugadas en un género específico**:
   - Permite identificar al usuario que ha jugado más horas en un género específico de juegos.

2. **Endpoint para Obtener Top 3 Juegos Más Recomendados por Usuarios para un Año**:
   - Identifica los tres juegos más recomendados para un año específico basándose en las reseñas de los usuarios.

3. **Endpoint para Detalles del Juego Recomendado**:
   - Proporciona información detallada sobre un juego recomendado específico, identificado por su ID.

4. **Endpoint para identificar los juegos que más le gusta a cada usuario y su sentimiento sobre el juego**:
   - Ofrece información detallada sobre un usuario específico, incluyendo los juegos que más le gusta y su sentimiento sobre cada juego.

#### Código de Sistema de Recomendación

```python
import pandas as pd

# Función para cargar el archivo de recomendaciones
def cargar_recomendaciones():
    return pd.read_csv('feel.csv')

# Función para obtener las recomendaciones para un item_id dado
def obtener_recomendaciones(item_id, df):
    recomendaciones = df[df['id'] == item_id]['Recomendaciones'].tolist()
    if not recomendaciones:
        return "No se encontraron recomendaciones para el item_id especificado"
    return recomendaciones

# Cargar el DataFrame
df = cargar_recomendaciones()

# Obtener recomendaciones para un item_id dado
item_id = 761140  # Cambia este valor por el item_id que quieras probar
recomendaciones = obtener_recomendaciones(item_id, df)
print(recomendaciones)
```

Este código define funciones para cargar un archivo CSV de recomendaciones y para obtener las recomendaciones para un `item_id` dado.

### Ejecución de main.py y Despliegue en FastAPI

Para ejecutar el archivo `main.py` y desplegar la API en FastAPI, sigue estos pasos:

#### 1. Configuración del Entorno Virtual

Para evitar conflictos de dependencias y mantener un entorno limpio, se recomienda crear un entorno virtual para ejecutar el proyecto. Puedes seguir estos pasos:

1. Abre una terminal en la ubicación donde se encuentra el archivo `main.py`.
2. Ejecuta el siguiente comando para crear un nuevo entorno virtual:

   ```bash
   python -m venv venv
   ```

3. Activa el entorno virtual. En Windows, ejecuta:

   ```bash
   venv\Scripts\activate
   ```

   Y en Linux/macOS, ejecuta:

   ```bash
   source venv/bin/activate
   ```

#### 2. Descarga de Archivos Originales

Descarga los archivos originales desde el siguiente enlace: [Google Drive](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj).

#### 3. Organización de Archivos Locales

Descomprime los archivos descargados y organízalos en una estructura de carpetas similar a la siguiente:

```
project_folder/
│
├── main.py
├── SistemReco/
│   └── feel.csv
└── Data_ETL/
    ├── data_games_clean.csv
    ├── data_users_items_clean.csv
    ├── user_reviews_clean.csv
    └── (otros archivos necesarios)
```

Asegúrate de que las rutas de los archivos en `main.py` correspondan a las rutas locales donde has guardado los archivos.

#### 4. Instalación de Dependencias

Instala las dependencias necesarias ejecutando el siguiente comando en la terminal:

```bash
pip install fastapi uvicorn pandas
```

#### 5. Ejecución de `main.py`

Finalmente, ejecuta el archivo `main.py` para iniciar el servidor FastAPI. Desde la terminal, navega hasta la ubicación del archivo `main.py` y ejecuta el siguiente comando:

```bash
uvicorn main:app --reload
```

Esto iniciará el servidor FastAPI en tu máquina local.

#### 6. Acceso a la API en FastAPI

Una vez que el servidor esté en funcionamiento, puedes acceder a los diferentes endpoints definidos en la API desde tu navegador o utilizando herramientas como cURL o Postman. Por ejemplo, puedes acceder a `http://127.0.0.1:8000/docs` para ver la documentación interactiva de la API generada automáticamente por FastAPI.

¡Y eso es todo! Ahora tienes tu API ejecutándose localmente y lista para proporcionar recomendaciones de videojuegos basadas en los endpoints definidos en `main.py`.


El proceso para llevar el sistema a producción en Render fue el siguiente:

1. **Preparación del Código**: Primero, aseguramos que nuestro código estuviera listo para la producción. Esto incluyó verificar que todos los archivos y dependencias estuvieran correctamente configurados y que el código estuviera libre de errores.

2. **Creación de la Cuenta en Render**: Nos registramos en la plataforma Render y creamos una cuenta para nuestro proyecto.

3. **Creación del Servicio Web**: Utilizamos la interfaz de Render para crear un nuevo servicio web. Configuramos las opciones necesarias, como el nombre del servicio, la configuración del entorno y las dependencias del proyecto.

4. **Configuración del Entorno**: Configuramos el entorno de Render para que coincida con nuestro entorno local. Esto incluyó la instalación de las mismas dependencias y la configuración de las variables de entorno si era necesario.

5. **Despliegue del Código**: Subimos nuestro código a Render utilizando Git o mediante la carga de archivos directamente en la plataforma. Render automáticamente construyó y desplegó nuestro servicio web.

6. **Pruebas y Depuración**: Una vez que el servicio estuvo desplegado, realizamos pruebas para asegurarnos de que todo funcionara correctamente. Si encontramos problemas, los depuramos y corregimos según fuera necesario.

7. **Documentación y Exposición de los Endpoints**: Utilizamos la documentación automática proporcionada por FastAPI para exponer nuestros endpoints y proporcionar una interfaz fácil de usar para interactuar con la API.

8. **Comunicación del Link de Render**: Finalmente, compartimos el enlace proporcionado por Render (https://ml-recsys-model.onrender.com/docs) con los interesados y los usuarios finales para que pudieran acceder a nuestra API en producción.

En resumen, el proceso implicó configurar nuestro código y entorno para la producción, desplegarlo en Render y realizar pruebas para garantizar su funcionamiento adecuado. Una vez que todo estuvo en orden, compartimos el enlace de Render para que otros pudieran acceder a nuestra aplicación en línea.

En conclusión, llevar nuestro sistema de recomendación de videojuegos a producción en Render fue un proceso enriquecedor y gratificante. Comenzamos preparando nuestro código y asegurándonos de que estuviera listo para la producción, lo que implicó configurar correctamente las dependencias y corregir cualquier error que pudiera surgir. Luego, con la ayuda de Render, creamos y configuramos nuestro servicio web, lo que nos permitió desplegar fácilmente nuestro código en línea.

Una vez que nuestro servicio estuvo en funcionamiento, realizamos pruebas exhaustivas para asegurarnos de que todo funcionara como se esperaba. Render proporcionó un entorno estable y confiable para nuestra aplicación, lo que facilitó la detección y corrección de problemas potenciales. La documentación automática generada por FastAPI nos permitió exponer nuestros endpoints de manera clara y accesible, lo que facilitó a los usuarios interactuar con nuestra API.

En general, el proceso de despliegue en Render fue fluido y eficiente, lo que nos permitió poner nuestra aplicación en producción rápidamente. Estamos satisfechos con el resultado final y confiamos en que nuestra API de recomendación de videojuegos proporcionará una experiencia valiosa para nuestros usuarios. Con Render, hemos logrado llevar nuestra aplicación a un entorno de producción estable y accesible, y estamos emocionados de ver cómo será recibida por la comunidad de jugadores.
