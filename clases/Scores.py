
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
        
        return df