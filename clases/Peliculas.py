import sys
sys.path.append('../')
import pandas as pd
import Helper as faux
import matplotlib.pyplot as plt

caracteresComplejos=["'","-"]


def genero_tabla_para_plot(df_tabla,generos):

    df_mov=df_tabla.copy()
    df_mov['year'] = df_mov['Release_Date'].dt.year
    genre_columns = ['year']+ generos #Si no especificaron generos se muestran todos
    df_genres = df_mov[genre_columns].copy()
    genre_by_year = df_genres.groupby('year').sum()
    genre_by_year=genre_by_year.loc[:, (genre_by_year != 0).any(axis=0)]  # Borrar columnas con valor 0
    return genre_by_year


class Pelicula:
    def __init__(self, nombre, anio, generos, id = None):
        
        self.nombre = nombre
        self.anio = anio
        self.generos = faux.elminoCaracterDeLista(generos,caracteresComplejos)
        self.id = id
    def __repr__(self):
        # Este método debe imprimir la información de esta película.
        return f'\n [{self.id}] {self.nombre} ({self.anio}) -{", ".join(map(str, self.generos))}-'
    
    def write_df(self, df):
        # Este método recibe el dataframe de películas y agrega la película
        # Si el id es None, toma el id más alto del DF y le suma uno. Si el 
        # id ya existe, no la agrega y devuelve un error.
        df_mov=df.copy()
        if self.id == None:
            self.id=df_mov.index.max()+1
        elif self.id in df_mov.index:
            print('Error: No se pudo agregar, id ya existente')
            return df_mov

        generosdict = {a:1 for a in self.generos} # genero un dict con esta estructura {'Adventure': 1, 'Comedy': 1, 'Animation': 1}
        new_row = {'Name': f'{self.nombre} ({self.anio})'}
        new_row.update(generosdict)
        TotalColumnasDF=df_mov.columns.tolist()
        RellenoConCerosDict={a : 0 for a in TotalColumnasDF if a not in new_row} # Completo el resto de los campos con 0
        new_row.update(RellenoConCerosDict)
        df_mov.loc[self.id] = new_row

        return df_mov

    def remove_from_df(self, df):
        # Borra del DataFrame el objeto contenido en esta clase.
        # Para realizar el borrado todas las propiedades del objeto deben coincidir
        # con la entrada en el DF. Caso contrario imprime un error.

        df_mov= df.copy()
        
        fila_a_borrar=self.filtrar_df(df_mov, id=self.id, nombre = self.nombre, anios = [self.anio,self.anio], generos = self.generos)
        if len(fila_a_borrar)==1:
            return df_mov.drop(fila_a_borrar.index)

        else:
            print("No existe en el df recibido una película exactamente igual a la que invoca esta acción")
            return df_mov
        
        return df_mov

    @classmethod
    def create_df_from_csv(cls, filename):
        # Este class method recibe el nombre de un archivo csv, valida su 
        # estructura y devuelve un DataFrame con la información cargada del
        # archivo 'filename'.
        ###
        df = pd.read_csv(filename)
        #Falta la validacion --> Hacerla por regex --> Hay algo más nativo ?
       
        df.set_index('id', inplace=True)
        df.columns = [col.replace(' ', '_') for col in df.columns]
        df['Release_Date'] = pd.to_datetime(df['Release_Date'], format='%d-%b-%Y')
        df=faux.eliminoCaracterDeColumnasDF(df,["'","-"])
       

        ###
        return df
    
    @classmethod
    def ConvertirAPeliculas(cls,df_mov):
        # Este class method recibe un df y devuelve un listado de peliculas
        lista_peliculas = []
        # Itera sobre cada fila del DataFrame
        for index, row in df_mov.iterrows():
            # Crea un objeto Pelicula con los datos de la fila actual
            generos_activos = df_mov.loc[index].loc[df_mov.loc[index] == 1].index.tolist()
            nombre=row['Name'][:row['Name'].rfind(' (')]
            anio=row['Release_Date'].year # aprovechando que tenemos una columna dateTime
            movie = Pelicula(nombre, anio, generos_activos, id=index)
            # Agrega el objeto Pelicula a la lista
            lista_peliculas.append(movie)

        return lista_peliculas

    @classmethod
    def filtrar_df(cls, df_mov, id=None, nombre = None, anios = None, generos = None):
        queryText=''

        if id!=None:
            queryText+='id=='+ str(id) + ' and '

        if nombre!=None:
            queryText+='Name.str.contains("' + nombre + '", case=False)'+ ' and '

        if anios!=None:
            desde,hasta=anios
            queryText+='Release_Date >= "' + str(desde)+'-01-01' +'" and Release_Date <= "'+ str(hasta)+'-12-31' + '"'+ ' and '

        if generos!=None:
            generos = faux.elminoCaracterDeLista(generos,caracteresComplejos)# corrijo caracteres problematicos '-
            generosR = [x + "== 1 or " for x in generos]
            generoRjoined= ''.join(generosR)
            queryText+= '('+generoRjoined[:-4]+')'
        else:
            queryText=queryText[:-5]#Se castea a todo menos los ultimos 5 caracteres ya que son un " and " adicional 
       
        return df_mov.query(queryText, engine="python")

    @classmethod
    def get_from_df(cls, df_mov, id=None, nombre = None, anios = None, generos = None):
    
        filtro=cls.filtrar_df(df_mov, id=id, nombre=nombre, anios=anios, generos=generos)
        return cls.ConvertirAPeliculas(df_mov=filtro)

    @classmethod
    def get_stats(cls,df_mov, anios=None, generos=None):
        # Este class method imprime una serie de estadísticas calculadas sobre
        # los resultados de una consulta al DataFrame df_mov. 
        # Las estadísticas se realizarán sobre las filas que cumplan con los requisitos de:
        # anios: [desde_año, hasta_año]
        # generos: [generos]
        # Las estadísticas son:
        filtro = cls.filtrar_df(df_mov, anios = anios, generos= generos)
        print(f'-Cantidad de peliculas en la selección:{filtro.shape[0]}\n')

        fecha_minima = filtro['Release_Date'].min()
        PelisMasAntigua=filtro[filtro['Release_Date'] == fecha_minima]
        if PelisMasAntigua.shape[0]==1:
            print(f'-Pelicula mas vieja:{cls.ConvertirAPeliculas(PelisMasAntigua)[0]}')
        else:
            print(f'-{PelisMasAntigua.shape[0]} películas comparten la fecha mas vieja:{cls.ConvertirAPeliculas(PelisMasAntigua)}')

        fecha_maxima = filtro['Release_Date'].max()
        PeliMasReciente=filtro[filtro['Release_Date'] == fecha_maxima]
        if PeliMasReciente.shape[0]==1:
            print(f'-\nPelicula mas reciente:\n{cls.ConvertirAPeliculas(PeliMasReciente)[0]}')
        else:
            print(f'-\n{PeliMasReciente.shape[0]} películas comparten la fecha mas reciente:{cls.ConvertirAPeliculas(PeliMasReciente)}')
        
        if generos==None:
            generos=filtro.drop(columns=['Release_Date']).columns[5:].tolist()
        generos = faux.elminoCaracterDeLista(generos,caracteresComplejos)
        tabla_para_plot = genero_tabla_para_plot(filtro,generos)
        faux.barplot_cantdad_año_generos(tabla_para_plot)
        # - Bar plots con la cantidad de películas por año/género.
 
        return
    
  

