import sys
sys.path.append('../') 
import pandas as pd
import numpy as np
import Helper as Faux
from datetime import datetime
from clases.Persona import Persona
from clases.Peliculas import Pelicula


class Score:
    def __init__(self, timestamp, puntuacion, idPelicula, idUsuario):
        
        self.timestamp = timestamp
        self.puntuacion = int(puntuacion)
        self.idPelicula = int(idPelicula)
        self.idUsuario = int(idUsuario)
    def __repr__(self):
        # Este método debe imprimir la información de esta película.
        return f'\n [ID Movie {self.idPelicula}] [ID Usuario{self.idUsuario}] - Califico: ({self.puntuacion}) en: -{self.timestamp}-'
    
    @classmethod
    def filtra_df(cls, df_sco,df_personas=None, df_peliculas=None, generoPersona=None, year_of_birth=None, anioReview=None, puntuacion=None, idPelicula=None, idUsuario=None, 
                  anioEstreno=None, generosPeliculas=None):
        
        queryText=''

        if idUsuario!=None:
            queryText+='user_id=='+ str(idUsuario) + ' and '
        if idPelicula!=None:
            queryText+='movie_id=='+ str(idPelicula) + ' and '
        if anioReview!=None:
            desde,hasta=anioReview
            queryText+='Date >= "' + str(desde)+'-01-01' +'" and Date <= "'+ str(hasta)+'-12-31' + '"'+ ' and '
        if puntuacion!=None:
            queryText+=f'rating=={puntuacion} and '
        
        queryText=queryText[:-5]#Se castea a todo menos los ultimos 5 caracteres ya que son un " and " adicional 

        if queryText=='':
            filtro = df_sco
        else:
            filtro = df_sco.query(queryText, engine="python")

        if isinstance(df_personas, pd.DataFrame) and (generoPersona!=None or year_of_birth!= None):
            df_persona_filtrado=Persona.filtrar_df(df_personas,Gender=generoPersona,yearOfBirth=year_of_birth)
            filtro=filtro[filtro['user_id'].isin(df_persona_filtrado['id'])]
            

        if  isinstance(df_peliculas, pd.DataFrame):
            df_peliculas_filtrado=Pelicula.filtrar_df(df_peliculas,anios=anioEstreno,generos=generosPeliculas)
            filtro=filtro[filtro['movie_id'].isin(df_peliculas_filtrado.index)]

        return filtro
    

    def write_df(self, df):
        # Este método recibe el dataframe de Scores y agrega el score de la instancia
        # Si el id movie y el id usuario coinciden  con una existente devuelve un error.
        df_sco=df.copy()
        filtro = self.filtra_df(df_sco)
        
        if len(filtro)==1:
            print("Se actualizará la calificacion ya exstente para esa pelicula y de este usuario")
            df_sco.at[filtro.index[0],'rating']=self.puntuacion
            df_sco.at[filtro.index[0],'Date']=self.timestamp

        elif len(filtro)==0:        
            new_row = {'user_id': self.idUsuario, 'movie_id': self.idPelicula, 'rating' : self.puntuacion, 'Date' : self.timestamp}
            df_sco=df_sco.append(new_row, ignore_index=True)

        else: 
            print("Hay varias calificaciones para esta pelicula y usuario, por lo que no se agregará la misma al df")
        
        return df_sco
    
    def remove_from_df(self, df_sco):

        fila_a_borrar=self.filtra_df(df_sco)
        if len(fila_a_borrar)==1:
            df_sco = df_sco.drop(fila_a_borrar.index)
        else:
           print("No existe en el df recibido una película exactamente igual a la que invoca esta acción")
        return df_sco
    
    @classmethod
    def ConvertirAScores(cls,df_sco):
        # Este class method recibe un df y devuelve un listado de peliculas
        lista_scores = []
        # Itera sobre cada fila del DataFrame
        for index, row in df_sco.iterrows():
            # Crea un objeto Pelicula con los datos de la fila actual
            puntuacion = row['rating']
            idPelicula=row['movie_id']
            idUsuario=row['user_id']
            timestamp=row['timestamp']
            score = Score(timestamp, puntuacion, idPelicula, idUsuario)
            # Agrega el objeto Pelicula a la lista
            lista_scores.append(score)

        return lista_scores
        
    @classmethod
    def create_df_from_csv(cls, filename):
        
        df = pd.read_csv(filename, index_col=0)
        df['Date'] = pd.to_datetime(df['Date'])
       
        return df
    
    @classmethod
    def get_from_df(cls, df_sco, anioReview=None, puntuacion=None, idPelicula=None, idUsuario=None):
           
        filtro= cls.filtra_df(df_sco, anioReview=anioReview, puntuacion=puntuacion, idPelicula=idPelicula, idUsuario=idUsuario)
        return cls.ConvertirAScores(filtro)
    
    @classmethod
    def obtener_rating_promedio_variable(cls, df_sco,variable='user_id'):
        # Estadísticas por Usuario/Película: Calificación promedio de usuario, Calificación promedio por película. 
       
        return df_sco.groupby(variable)['rating'].mean().reset_index()
        
    @classmethod
    def puntuacion_año_genero(cls,df_peliculas,df_sco,generosDeseadosList, anios=None):
       
        #Mergeo Scores y Peliculas y agrego la columna year
        movies_agrupado=df_sco.groupby('movie_id')['rating'].mean().reset_index()
        df_peliculas['year'] = df_peliculas['Release_Date'].dt.year
        merged_df = pd.merge(movies_agrupado[['movie_id','rating']], df_peliculas.iloc[:, 3:], left_on='movie_id',right_index=True, how='inner')
        
        # Traslado el valor de rating a cada genero al que pertenece
        merged_df.iloc[:, 3:] = merged_df.iloc[:, 3:].astype(float)
        merged_df.apply(lambda row: Faux.trasladar_rating_a_columnas_generos(row, merged_df), axis=1)

        #Me quedo unicamente con la columna año y todos los generos promediados
        dfPlot=merged_df.groupby(['year'])[merged_df.iloc[:, 3:-1].columns.tolist()].mean().reset_index()
        
        #Filtro anios especificados
        if anios != None:
            dfPlot = dfPlot[(dfPlot['year'] >= anios[0]) & (dfPlot['year'] <= anios[1])]
        dfPlotInterpolado=dfPlot.interpolate(inplace=False)

        Faux.plot_lineas_rating_añoPelicula_generos(dfPlot ,dfPlotInterpolado ,generosDeseadosList).show
        return

    @classmethod
    def puntuacion_edad_genero(cls,df_personas,df_sco):
        
        users_agrupado=df_sco.groupby('user_id')['rating'].mean().reset_index()
        merged_users_scores_df = pd.merge(users_agrupado, df_personas[['id','year_of_birth','Gender']],right_on='id', left_on="user_id", how='inner')
        merged_users_scores_df['age'] = datetime.now().year - merged_users_scores_df['year_of_birth']
        merged_users_scores_df_grouped=merged_users_scores_df.groupby(['Gender','age'])['rating'].mean().reset_index()

        #Grafico de Barras
        Faux.barplot_comparativo_edad_genero_rating(merged_users_scores_df_grouped)

        #Distribution Plot
        Faux.kdeplot_edad_genero_rating(merged_users_scores_df)
        return

    @classmethod
    def puntuacion_ocupacion_rating(cls,df_usuarios,df_sco):
        users_agrupado=df_sco.groupby('user_id')['rating'].mean().reset_index()
        merged_users_scores_df = pd.merge(users_agrupado, df_usuarios,right_on='id', left_on="user_id", how='inner')
        Faux.HorizontalBarplot_usuario_rating(merged_users_scores_df)
        return
