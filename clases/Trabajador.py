
import pandas as pd
import Funciones_Auxiliares as faux

caracteresComplejos=["'","-"]

class Trabajador:
    def __init__(self, puesto, categoria, horarioTrabajo, fechaAlta, id=None):
        self.id = id
        self.puesto = puesto
        self.categoria = categoria
        self.horarioTrabajo = horarioTrabajo
        self.fechaAlta = fechaAlta

    def __repr__(self):
        # Este método debe imprimir la información de este trabajador.
        return f'\n {self.id} - {self.fechaAlta} - {self.puesto} - {self.categoria} - {self.horarioTrabajo}'
    
    def write_df(self, df_mov):
        # Este método recibe el dataframe de Trabajadores y agrega el nuevo trabajador
        # Si el id es None, toma el id más alto del DF y le suma uno. Si el 
        # id ya existe, no la agrega y devuelve un error.

        if self.id == None:
            self.id=df_mov['id'].max()+1
        elif self.id in df_mov['id'].values:
            print('Error: No se pudo agregar, id ya existente')
            return df_mov

        new_row = {'id': self.id, 'Position': self.puesto, 'Category': self.categoria, 'Working Hours': self.horarioTrabajo, 'Start Date': self.fechaAlta}
        new_row_df = pd.DataFrame([new_row])
        df_mov = pd.concat([df_mov, new_row_df], ignore_index=True)
        
        # Guardar el DataFrame actualizado en el archivo CSV
        df_mov.to_csv('../data/trabajadores.csv', index=False)
        
        return df_mov

    # def remove_from_df(self, df_mov):
    #     # Borra del DataFrame el objeto contenido en esta clase.
    #     # Para realizar el borrado todas las propiedades del objeto deben coincidir
    #     # con la entrada en el DF. Caso contrario imprime un error.
        
    #     fila_a_borrar=self.get_from_df(df_mov, id=self.id, nombre = self.nombre, anios = [self.anio,self.anio], generos = self.generos)
    #     if len(fila_a_borrar)==1:
    #         return df_mov.drop(df_mov[df_mov['id'] == fila_a_borrar[0].id].index)

    #     else:
    #         print("No existe en el df recibido una película exactamente igual a la que invoca esta acción")
    #         return df_mov
        
        return df_mov

    @classmethod
    def create_df_from_csv(cls, filename):
        # Este class method recibe el nombre de un archivo csv, valida su 
        # estructura y devuelve un DataFrame con la información cargada del
        # archivo 'filename'.
        
        df = pd.read_csv(filename)
        
        df['DateNorm'] = pd.to_datetime(df['Start Date'], format='%Y-%m-%d')
        
        df=faux.eliminoCaracterDeColumnasDF(df,["'","-"])

        return df
    
    @classmethod
    def convertir_a_trabajadores(cls,df_mov):
        # Este class method recibe un df y devuelve un listado de trabajadores
        lista_trabajadores = []
        # Itera sobre cada fila del DataFrame
        for index, row in df_mov.iterrows():
            # Crea un objeto Trabajador con los datos de la fila actual
            puesto = row['Position'][:row['Position'].rfind(' (')]
            categoria = row['Category'][:row['Category'].rfind(' (')]
            horarioTrabajo = row['Working Hours'][:row['Working Hours'].rfind(' (')]
            fechaAlta = row['Start Date'][:row['Start Date'].rfind(' (')]

            # Pasa los argumentos usando el nombre de los parámetros
            trabajador = Trabajador(id=row['id'], fechaAlta=fechaAlta, puesto=puesto, categoria=categoria, horarioTrabajo=horarioTrabajo)
            # Agrega el objeto Trabajador a la lista
            lista_trabajadores.append(trabajador)

        return lista_trabajadores

    # @classmethod
    # def filtrar_df(cls, df_mov, id=None, nombre = None, anios = None, generos = None):
    #     queryText=''

    #     if id!=None:
    #         queryText+='id=='+ str(id) + ' and '

    #     if nombre!=None:
    #         queryText+='Name.str.contains("' + nombre + '", case=False)'+ ' and '

    #     if anios!=None:
    #         desde,hasta=anios
    #         queryText+='DateNorm >= "' + str(desde)+'-01-01' +'" and DateNorm <= "'+ str(hasta)+'-12-31' + '"'+ ' and '

    #     if generos!=None:
    #         generos = faux.elminoCaracterDeLista(generos,caracteresComplejos)# corrijo caracteres problematicos '-
    #         generosR = [x + "== 1 and " for x in generos] 
    #         queryText+=''.join(generosR)
        
    #    #Se castea a todo menos los ultimos 5 caracteres ya que son un " and " adicional con el que siempre termina la query
    #     return df_mov.query(queryText[:-5], engine="python")

    # @classmethod
    # def get_from_df(cls, df_mov, id=None, nombre = None, anios = None, generos = None):
    
    #     filtro=cls.filtrar_df(df_mov, id=id, nombre=nombre, anios=anios, generos=generos)
    #     return cls.ConvertirAPeliculas(df_mov=filtro)

    # @classmethod
    # def get_stats(cls,df_mov, anios=None, generos=None):
    #     # Este class method imprime una serie de estadísticas calculadas sobre
    #     # los resultados de una consulta al DataFrame df_mov. 
    #     # Las estadísticas se realizarán sobre las filas que cumplan con los requisitos de:
    #     # anios: [desde_año, hasta_año]
    #     # generos: [generos]
    #     # Las estadísticas son:
    #     filtro = cls.filtrar_df(df_mov, anios = anios, generos= generos)

    #     fecha_minima = filtro['DateNorm'].min()
    #     PelisMasAntigua=filtro[filtro['DateNorm'] == fecha_minima]
    #     if PelisMasAntigua.shape[0]==1:
    #         print(f'Pelicula mas vieja:\n{cls.ConvertirAPeliculas(PelisMasAntigua)[0]}')
    #     else:
    #         print(f'{PelisMasAntigua.shape[0]} películas comparten la fecha mas vieja:\n{cls.ConvertirAPeliculas(PelisMasAntigua)}')

    #     fecha_maxima = filtro['DateNorm'].max()
    #     PeliMasReciente=filtro[filtro['DateNorm'] == fecha_maxima]
    #     if PeliMasReciente.shape[0]==1:
    #         print(f'\nPelicula mas reciente:\n{cls.ConvertirAPeliculas(PeliMasReciente)[0]}')
    #     else:
    #         print(f'{PelisMasAntigua.shape[0]} películas comparten la fecha mas reciente:\n{cls.ConvertirAPeliculas(PeliMasReciente)}')
    #     # - Datos película más vieja
    #     # - Datos película más nueva
    #     # - Bar plots con la cantidad de películas por año/género.
    #     # - Cantidad de películas totales.
    #     return
    
  

