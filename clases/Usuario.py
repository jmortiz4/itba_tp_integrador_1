
import pandas as pd
import Persona as Persona

class Usuario(Persona):
    
    def __init__(self, id=None, fecha_nac=None, genero=None, cod_postal=None, ocupacion=None, fecha_alta=None, fullname=None):
        super().__init__(id=id, FullName=fullname, fecha_nac=fecha_nac, Gender=genero, cod_postal=cod_postal)
        self.ocupacion = ocupacion
        self.fecha_alta = fecha_alta

    def __repr__(self):
        # Imprime informacion del usuario
        return f'\n {Persona.__repr__(self)}, ocupacion={self.ocupacion}, fecha_alta={self.fecha_alta}'

    
    @classmethod
    def create_df_from_csv(cls, filename):
        # Este class method recibe el nombre de un archivo csv, valida su 
        # estructura y devuelve un DataFrame con la información cargada del
        # archivo 'filename'.
        ###
        df = pd.read_csv(filename)
        df['Active Since'] = pd.to_datetime(df['Active Since'], format='%Y-%m-%d %H:%M:%S')
        df = df.rename(columns={'Active Since':'fecha_alta','Occupation':'ocupacion'})
        return df

    @classmethod
    def filtrar_df(cls, df, id=None, ocupacion = None):
        queries=[]

        if id!=None:
            queries.append(f'id=={str(id)}')

        if ocupacion!=None:
            queries.append(f'ocupacion=="{ocupacion}"')

        query_text = ' and '.join(queries)
        return df.query(query_text, engine="python")


    @classmethod
    def ConvertirAUsuarios(cls,df):
        # Este class method recibe un df y devuelve un listado de peliculas
        lista_usuarios = []
        # Itera sobre cada fila del DataFrame
        for index,row in df.iterrows():
            # Crea un objeto Usuario con los datos de la fila actual
            id = row['id']
            ocupacion = row['ocupacion']
            fecha_alta = row['fecha_alta']
            usuario = Usuario(id=id, ocupacion=ocupacion, fecha_alta=fecha_alta)
            # Agrega el objeto Pelicula a la lista
            lista_usuarios.append(usuario)
        return lista_usuarios

    @classmethod
    def get_from_df(cls, df,id=None, ocupacion = None, fecha_alta = None):
    
        filtro=cls.filtrar_df(df, id=id, ocupacion=ocupacion)
        if len(filtro)==0:
            print("No se encontraron usuarios con esos criterios")
            return None
        else:
            return cls.ConvertirAUsuarios(df=filtro)
    
    def write_df(self, df):
        if self.id == None:
            self.id=df['id'].max()+1
        elif self.id in df['id'].values:
            print('Error: No se pudo agregar, id ya existente')
            return df

        new_row = {'id': self.id, 'ocupacion': self.ocupacion, 'fecha_alta': self.fecha_alta}
        new_row_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_row_df], ignore_index=True)
        
        # Guardar el DataFrame actualizado en el archivo CSV
        df.to_csv('data/usuarios_updated.csv', index=False)
        
        return df