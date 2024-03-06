from fastapi import FastAPI, HTTPException, Query
from fastapi import FastAPI
import pandas as pd
from flask import Flask, request, jsonify

# Inicializar la aplicación FastAPI
app = FastAPI()


## **1. Endpoint para obtener al usuario con más horas jugadas en un género específico**

# Cargar los datos
df_games = pd.read_csv(r'C:\Users\pc-admin\Documents\ML_RecSys_Model\Data_ETL\data_games_clean.csv')
df_users_items = pd.read_csv(r'C:\Users\pc-admin\Documents\ML_RecSys_Model\Data_ETL\data_users_items_clean.csv')

# Definir el Endpoint
@app.get("/most_played_user_in_genre")
async def most_played_user_in_genre(genre: str):
    # Filtrar los juegos por el género específico
    juegos_genero = df_games[df_games['tags'].str.contains(genre)]

    # Unir los datos de los juegos con los datos de usuarios e items
    df = pd.merge(df_users_items, juegos_genero, left_on='item_id', right_on='id')

    # Agrupar por usuario y sumar las horas jugadas
    horas_por_usuario = df.groupby('user_id')['hours_game'].sum()

    # Encontrar al usuario con más horas jugadas en el género específico
    usuario_mas_horas = horas_por_usuario.idxmax()
    horas_mas_jugadas = horas_por_usuario.max()

    return {"genre": genre, "user_id": usuario_mas_horas, "hours_played": horas_mas_jugadas}


## **2. Endpoint para Obtener Top 3 Juegos Más Recomendados por Usuarios para un Año:**

# Cargar los datos
df_reviews = pd.read_csv(r'C:\Users\pc-admin\Documents\ML_RecSys_Model\Data_ETL\user_reviews_clean.csv')
df_games = pd.read_csv(r'C:\Users\pc-admin\Documents\ML_RecSys_Model\Data_ETL\data_games_clean.csv')

# Definir el Endpoint
@app.get("/top_games/{year}")
async def get_top_games(year: int):
    def top_3_games(year):
        # Filtrar las recomendaciones para el año especificado
        reviews_year = df_reviews[df_reviews['year'] == year]
        
        # Contar las recomendaciones para cada juego
        top_games = reviews_year['item_id'].value_counts().head(3)
        
        # Obtener los IDs de los juegos más recomendados
        top_game_ids = top_games.index.tolist()
        
        # Obtener los nombres de los juegos más recomendados
        top_game_names = df_games[df_games['id'].isin(top_game_ids)]['app_name'].tolist()
        
        # Combinar IDs y nombres de juegos
        top_games_info = [{'id': game_id, 'name': game_name} for game_id, game_name in zip(top_game_ids, top_game_names)]
        
        return top_games_info
    
    return top_3_games(year)



## **3. Endpoint para Detalles del Juego Recomendado:**

# Cargar el conjunto de datos de juegos
df_games = pd.read_csv('C:\\Users\\pc-admin\\Documents\\ML_RecSys_Model\\Data_ETL\\data_games_clean.csv')

# Definir el Endpoint
@app.get("/recommended_game/{game_id}")
async def get_recommended_game_details(game_id: int):
    # Buscar el juego recomendado por su ID
    recommended_game = df_games[df_games['id'] == game_id]
    
    if recommended_game.empty:
        return {'error': 'Juego no encontrado'}
    
    # Obtener los detalles específicos del juego recomendado
    game_details = {
        'id': int(recommended_game['id'].values[0]),
        'app_name': recommended_game['app_name'].values[0],
        'tags': recommended_game['tags'].values[0],
        'specs': recommended_game['specs'].values[0],
        'year': int(recommended_game['year'].values[0])  # Convertir a entero
        # Agregar más detalles según sea necesario
    }
    
    return game_details



## **4. Endpoint para identificar año con menor horas jugadas y juegos menos populares:**


# Cargar el dataset de juegos
df_games = pd.read_csv('C:\\Users\\pc-admin\\Documents\\ML_RecSys_Model\\Data_ETL\\data_games_clean.csv')

# Cargar el dataset de horas jugadas por usuario
df_hours = pd.read_csv('C:\\Users\\pc-admin\\Documents\\ML_RecSys_Model\\Data_ETL\\data_users_items_clean.csv')

# Unir los datasets de horas jugadas y juegos
merged_df = pd.merge(df_hours, df_games, left_on='item_id', right_on='id')

# Definir el endpoint para obtener el año con la menor cantidad total de horas jugadas y los 10 juegos con menor uso
@app.get("/stats")
async def get_stats():
    # Agrupar por año y sumar las horas jugadas
    total_hours_per_year = merged_df.groupby('year')['hours_game'].sum()
    # Encontrar el año con la menor cantidad total de horas jugadas
    year_with_least_hours = total_hours_per_year.idxmin()
    least_hours_played = total_hours_per_year.min()
    
    # Calcular las horas jugadas por juego
    total_hours_per_game = merged_df.groupby('app_name')['hours_game'].sum()
    # Encontrar los 10 juegos con menor uso
    bottom_10_games = total_hours_per_game.nsmallest(10)
    
    return {
        "year_with_least_hours": int(year_with_least_hours),  # Convertir a entero
        "least_hours_played": float(least_hours_played),  # Convertir a flotante
        "bottom_10_games": bottom_10_games.reset_index().to_dict()  # Resetear el índice para evitar problemas
    }



## **5. Enpoint para identificar los juegos que mas le gusta a cada usuario y su sentimiento sobre el juego**

# Cargar los DataFrames
df_users_items = pd.read_csv(r'C:\Users\pc-admin\Documents\ML_RecSys_Model\Data_ETL\data_users_items_clean.csv')
df_user_reviews = pd.read_csv(r'C:\Users\pc-admin\Documents\ML_RecSys_Model\Data_ETL\user_reviews_clean.csv')


# Definir el Endpoint para obtener la información del usuario
@app.get("/user_info/{user_id}")
async def get_user_info(user_id: str):
    # Filtrar el DataFrame para obtener la información del usuario específico
    user_info = df_users_items[df_users_items['user_id'] == user_id]
    
    # Verificar si se encontró el usuario
    if not user_info.empty:
        # Obtener información del usuario
        total_hours_played = user_info['hours_game'].sum()
        num_games_played = len(user_info)
        
        # Obtener los juegos más jugados por el usuario
        top_games = user_info.groupby('item_id').size().sort_values(ascending=False).head(3)
        top_games_info = []
        for game_id, _ in top_games.items():
            # Verificar si el juego tiene una entrada en el DataFrame de reseñas
            if game_id in df_user_reviews.index:
                # Obtener el sentimiento del usuario sobre el juego
                game_sentiment = df_user_reviews.loc[game_id, 'sentiment_analysis']
            else:
                game_sentiment = None
                
            top_games_info.append({
                'game_id': game_id,
                'sentiment': game_sentiment
            })
        
        # Crear un diccionario con la información del usuario
        user_dict = {
            'user_id': user_id,
            'total_hours_played': total_hours_played,
            'num_games_played': num_games_played,
            'top_games': top_games_info
        }
        return user_dict
    else:
        return {'message': 'User not found'}




# Función para cargar el archivo de recomendaciones


def cargar_recomendaciones():
    return pd.read_csv(r'C:\Users\pc-admin\Documents\ML_RecSys_Model\SistemReco\feel.csv')

# Función para obtener las recomendaciones para un item_id dado
def obtener_recomendaciones(item_id, df):
    recomendaciones = df[df['id'] == item_id]['Recomendaciones'].tolist()
    if not recomendaciones:
        raise HTTPException(status_code=404, detail="No se encontraron recomendaciones para el item_id especificado")
    return recomendaciones

# Endpoint para obtener recomendaciones
@app.get("/recommendations/{item_id}")
async def get_recommendations(item_id: int):
    df = cargar_recomendaciones()
    recomendaciones = obtener_recomendaciones(item_id, df)
    return {"item_id": item_id, "recomendaciones": recomendaciones}
