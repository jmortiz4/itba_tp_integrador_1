import sys
sys.path.append('../') 
import pandas as pd
import Helper as faux

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
    
    def write_df(self, df_trabajadores):
        # Este método recibe el dataframe de Trabajadores y agrega el nuevo trabajador
        # Si el id es None, toma el id más alto del DF y le suma uno. Si el 
        # id ya existe, no la agrega y devuelve un error.

        if self.id == None:
            self.id=df_trabajadores['id'].max()+1
        elif self.id in df_trabajadores['id'].values:
            print('Error: No se pudo agregar, id ya existente')
            return df_trabajadores

        new_row = {'id': self.id, 'Position': self.puesto, 'Category': self.categoria, 'Working_Hours': self.horarioTrabajo, 'Start_Date': self.fechaAlta}
        new_row_df = pd.DataFrame([new_row])
        df_trabajadores = pd.concat([df_trabajadores, new_row_df], ignore_index=True)
        
        # Guardar el DataFrame actualizado en el archivo CSV
        df_trabajadores.to_csv('../data/trabajadores.csv', index=False)
        
        return df_trabajadores

    def remove_from_df(self, df_trabajadores):
        # Borra del DataFrame el objeto contenido en esta clase.
        df_trabajadores = df_trabajadores[df_trabajadores['id'] != self.id]
        
        # Guardar el DataFrame actualizado en el archivo CSV
        df_trabajadores.to_csv('../data/trabajadores.csv', index=False)

        return df_trabajadores

    @classmethod
    def create_df_from_csv(cls, filename):
        # Este class method recibe el nombre de un archivo csv, valida su 
        # estructura y devuelve un DataFrame con la información cargada del
        # archivo 'filename'.
        
        df = pd.read_csv(filename)
        df = df.rename(columns={'Working Hours': 'Working_Hours'})
        df = df.rename(columns={'Start Date': 'Start_Date'})

        
        df=faux.eliminoCaracterDeColumnasDF(df,["'","-"])

        return df
    
    @classmethod
    def convertir_a_trabajadores(cls,df_trabajadores):
        # Este class method recibe un df y devuelve un listado de trabajadores
        lista_trabajadores = []
        # Itera sobre cada fila del DataFrame
        for index, row in df_trabajadores.iterrows():
            # Crea un objeto Trabajador con los datos de la fila actual
            puesto = row['Position']
            categoria = row['Category']
            horarioTrabajo = row['Working_Hours']
            fechaAlta = row['Start_Date']

            # Pasa los argumentos usando el nombre de los parámetros
            trabajador = Trabajador(id=row['id'], fechaAlta=fechaAlta, puesto=puesto, categoria=categoria, horarioTrabajo=horarioTrabajo)
            # Agrega el objeto Trabajador a la lista
            lista_trabajadores.append(trabajador)

        return lista_trabajadores

    @classmethod
    def filtrar_df(cls, df_trabajadores, id=None, puesto = None, categoria = None, horarioTrabajo = None):
        if not isinstance(df_trabajadores, pd.DataFrame):
            print("Error: df_trabajadores no es un DataFrame válido")
            return None
        
        queryText=''

        if id!=None:
            queryText+='id=='+ str(id) + ' and '

        if puesto!=None:
            queryText+='Position.str.contains("' + puesto + '", case=False)'+ ' and '

        if categoria!=None:
            queryText+='Category.str.contains("' + categoria + '", case=False)'+ ' and '

        if horarioTrabajo!=None:
            queryText += "Working_Hours.str.contains('" + horarioTrabajo + "', case=False)"+ ' and '
        
        # Se elimina el último "and" si existe
        if queryText.endswith(' and '):
            queryText = queryText[:-5]

       #Se castea a todo menos los ultimos 5 caracteres ya que son un " and " adicional con el que siempre termina la query
        return df_trabajadores.query(queryText, engine="python")
    

    @classmethod
    def get_from_df(cls, df_trabajadores, id=None, puesto = None, categoria = None, horarioTrabajo = None):
    
        filtro=cls.filtrar_df(df_trabajadores, id=id, puesto=puesto, categoria=categoria, horarioTrabajo=horarioTrabajo)
        return cls.convertir_a_trabajadores(df_trabajadores=filtro)

    # @classmethod
    # def get_stats(cls,df_trabajadores, anios=None, generos=None):
    #     # Este class method imprime una serie de estadísticas calculadas sobre
    #     # los resultados de una consulta al DataFrame df_trabajadores. 
    #     # Las estadísticas se realizarán sobre las filas que cumplan con los requisitos de:
    #     # anios: [desde_año, hasta_año]
    #     # generos: [generos]
    #     # Las estadísticas son:
    #     filtro = cls.filtrar_df(df_trabajadores, anios = anios, generos= generos)

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
    
  

