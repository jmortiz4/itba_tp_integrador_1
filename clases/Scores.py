
import pandas as pd
import matplotlib.pyplot as plt


class Score:
    def __init__(self, timestamp, puntuacion, idPelicula, idUsuario):
        
        self.timestamp = timestamp
        self.puntuacion = int(puntuacion)
        self.idPelicula = int(idPelicula)
        self.idUsuario = int(idUsuario)
    def __repr__(self):
        # Este método debe imprimir la información de esta película.
        return f'\n [ID Movie {self.idPelicula}] [ID Usuario{self.idUsuario}] - Califico: ({self.puntuacion}) en: -{self.timestamp}-'
    
    def filtra_df(self,df_sco):
        return df_sco[(df_sco['user_id'] == self.idUsuario) & (df_sco['movie_id'] == self.idPelicula)]
    

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
    def create_df_from_csv(cls, filename):
        # Este class method recibe el nombre de un archivo csv, valida su 
        # estructura y devuelve un DataFrame con la información cargada del
        # archivo 'filename'.
        ###
        df = pd.read_csv(filename, index_col=0)
        df['Date'] = pd.to_datetime(df['Date'])
       
        return df
    
    @classmethod
    def get_from_df(cls, df_sco, anios=None, puntuacion=None, idPelicula=None, idUsuario=None):
        queryText=''

        if idUsuario!=None:
            queryText+='user_id=='+ str(idUsuario) + ' and '
        if idPelicula!=None:
            queryText+='movie_id=='+ str(idPelicula) + ' and '
        if anios!=None:
            desde,hasta=anios
            queryText+='Date >= "' + str(desde)+'-01-01' +'" and Date <= "'+ str(hasta)+'-12-31' + '"'+ ' and '
        if puntuacion!=None:
            queryText+=f'rating=={puntuacion} and '
        
        queryText=queryText[:-5]#Se castea a todo menos los ultimos 5 caracteres ya que son un " and " adicional 
    
        return df_sco.query(queryText, engine="python")
    
    @classmethod
    def obtener_rating_promedio_variable(cls, df_sco,variable='user_id'):
        # Estadísticas por Usuario/Película: Calificación promedio de usuario, Calificación promedio por película. 
       
        return df_sco.groupby(variable)['rating'].mean().reset_index()
        
            

        #- Scores: Puntuación promedio de usuario(s) por año(de película)/género. Puntuación promedio de películas por género de usuario(sexo)/rango etáreo/Ocupación.