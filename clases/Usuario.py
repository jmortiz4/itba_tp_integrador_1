import pandas as pd
import sys
sys.path.append('../')
import Helper as faux
from clases.Persona import Persona

class Usuario(Persona):
    
    def __init__(self, anho_nac=None, genero=None, cod_postal=None, ocupacion=None, fecha_alta=None, fullname=None,id=None):
        super().__init__(id=id, fullname=fullname, yearOfBirth=anho_nac, gender=genero, zipcode=cod_postal)
        if id is not None:
            # Si se proporciona un ID, cargamos los datos de la persona
            personas = Persona.ConvertirAPersonas(Persona.create_df_from_csv("../data/personas.csv"))
            for p in personas:
                if p.id == id: 
                    super().__init__(id=p.id, fullname=p.fullName, yearOfBirth=p.yearOfBirth, gender=p.gender, zipcode=p.zipcode)
        
        else:
            super().__init__(id=id, fullname=fullname, yearOfBirth=anho_nac, gender=genero, zipcode=cod_postal)
        

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
        for _,row in df.iterrows():
            # Crea un objeto Usuario con los datos de la fila actual
            ocupacion = row['ocupacion']
            fecha_alta = row['fecha_alta']
            id = row['id']
            usuario = Usuario(id=id, ocupacion=ocupacion, fecha_alta=fecha_alta)
            # Agrega el objeto Pelicula a la lista
            lista_usuarios.append(usuario)
        return lista_usuarios

    @classmethod
    def get_from_df(cls, df,id=None, ocupacion = None):
    
        filtro=cls.filtrar_df(df, id=id, ocupacion=ocupacion)
        if len(filtro)==0:
            print("No se encontraron usuarios con esos criterios")
            return None
        else:
            return cls.ConvertirAUsuarios(df=filtro)
    
    
    def write_df(self, df_usuarios, df_personas):


        if self.id == None:
            self.id=df_usuarios['id'].max()+1
        elif self.id in df_usuarios['id'].values:
            print('Error: No se pudo agregar, id ya existente')
            return df_usuarios
        
        new_row = {'id':self.id, 'ocupacion': self.ocupacion, 'fecha_alta': self.fecha_alta}
        new_row_df = pd.DataFrame([new_row])
        #df_usuarios.loc[self.id] = new_row
        df_usuarios = pd.concat([df_usuarios,new_row_df],ignore_index = True)

        new_row = {'id':self.id,'Full_Name': self.fullName, 'year_of_birth' : self.yearOfBirth, 'Gender' : self.gender, 'Zip_Code' : self.zipcode }
        new_row_df = pd.DataFrame([new_row])
        df_personas = pd.concat([df_personas,new_row_df],ignore_index = True)

        return df_usuarios,df_personas
    
    def remove_from_df(self, df):
        # Borra del DataFrame el objeto contenido en esta clase.
        # Para realizar el borrado todas las propiedades del objeto deben coincidir
        # con la entrada en el DF. Caso contrario imprime un error.
        df_usuarios= df.copy()
        
        fila_a_borrar=self.filtrar_df(df_usuarios, id=self.id, ocupacion = self.ocupacion)
        if len(fila_a_borrar)==1:
            return df_usuarios.drop(fila_a_borrar.index)

        else:
            print("No existe en el df recibido una persona exactamente igual a la que invoca esta acción")
            return df_usuarios

    @classmethod
    def persistir_df(cls, df_personas, df_usuarios):
       # Guardar los dataframes actualizados en los archivos CSV
       dict_replace = { 'ocupacion':'Occupation', 'fecha_alta':'Active Since'}
       df_usuarios = df_usuarios.replace(columns=dict_replace)
       df_usuarios.to_csv('../data/usuarios.csv', index=False)
       df_personas.to_csv('../data/personas.csv', index=False)

       return

    @classmethod
    def get_stats(cls, df_usuarios, dfpersonas, ocupacionesList=None, aniosDeInteres=None):
        
        dfpersonasLocal=dfpersonas.copy()
        dfpersonasLocal = Persona.filtrar_df(dfpersonasLocal , yearOfBirth=aniosDeInteres)
        merged_users_personas=pd.merge(df_usuarios['ocupacion'], dfpersonasLocal['year_of_birth'], left_index=True, right_index=True, how='inner')
        

        if ocupacionesList!=None: 
            df_filtrado1 = merged_users_personas[merged_users_personas['ocupacion'].isin(ocupacionesList)]
        else:
            df_filtrado1=merged_users_personas

        TotalUsuarios=df_filtrado1.shape[0]
        print("El Total de Usuarios es: ",TotalUsuarios)

        grouped_data = df_filtrado1.groupby(["ocupacion", "year_of_birth"]).size().reset_index(name="count")
        grouped_data['ocupacion'] = grouped_data['ocupacion'].str.lower().str.title()
        faux.heatmap_ocupacion_nacimiento(grouped_data)

        return

    