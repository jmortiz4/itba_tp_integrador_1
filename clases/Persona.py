import pandas as pd
import Funciones_Auxiliares as faux


# Personas: Cantidad de personas por año de nacimiento y Género. Cantidad total de personas.
class Persona:
    def __init__(self, id, FullName, yearOfBirth, Gender , ZipCode):
        self.id = id
        self.FullName = FullName
        self.yearOfBirth = yearOfBirth
        self.Gender = Gender
        self.ZipCode = ZipCode
        
    def __repr__(self):
        # Este método debe imprimir la información de esta persona.
        return f'\n [{self.id}] {self.FullName} {self.yearOfBirth} {self.Gender} {self.ZipCode} ' 
    
    def write_df(self, df_persona):
        # Este método recibe el dataframe de personas y agrega personas
        # Si el id es None, toma el id más alto del DF y le suma uno. Si el 
        # id ya existe, no la agrega y devuelve un error.

        if self.id == None:
            self.id=df_persona['id'].max()+1
        elif self.id in df_persona['id'].values:
            print('Error: No se pudo agregar, id ya existente')
            return df_persona

    def remove_from_df(self, df_persona):
        # Borra del DataFrame el objeto contenido en esta clase.
        # Para realizar el borrado todas las propiedades del objeto deben coincidir
        # con la entrada en el DF. Caso contrario imprime un error.
    
        
        fila_a_borrar=self.get_from_df(df_persona, id=self.id, FullName = self.FullName, yearOfBirth = self.yearOfBirth, Gender = self.Gender, ZipCode = self.ZipCode)
        if len(fila_a_borrar)==1:
            return df_persona.drop(df_persona[df_persona['id'] == fila_a_borrar[0].id].index)

        else:
            print("No existe en el df recibido una persona exactamente igual a la que invoca esta acción")
            return df_persona

    @classmethod
    def create_df_from_csv(cls, file_personas):
        # Este class method recibe el nombre de un archivo csv, valida su 
        # estructura y devuelve un DataFrame con la información cargada del
        # archivo 'filename'.
        ###
        df = pd.read_csv(file_personas)
        #Falta la validacion --> Hacerla por regex --> Hay algo más nativo ?
        df['DateNorm'] = pd.to_datetime(df['Release Date'], format='%d-%b-%Y')
        
        df=faux.eliminoCaracterDeColumnasDF(df,["'","-"])
       
        ###
        return df
    
    @classmethod
    def ConvertirAPersonas(cls,df_persona):
        # Este class method recibe un df y devuelve un listado de personas
        lista_personas = []
        # Itera sobre cada fila del DataFrame
        for index, row in df_persona.iterrows():
            # Crea un objeto Persona con los datos de la fila actual
            
            FullName=row['Full Name'][:row['Full Name'].rfind(' (')]
            # Una forma de calcular el año --> anio=int(row['Name'][row['Name'].rfind(' (')+2:-1])
            yearOfBirth=row['DateNorm'].year # aprovechando que tenemos una columna dateTime
            Gender=row['Gender'][:row['Gender'].rfind(' (')]
            ZipCode=row['Zip Code'][:row['Zip Code'].rfind(' (')]
            person = Persona(FullName, yearOfBirth, Gender , ZipCode, id=row['id'])
            # Agrega el objeto Pelicula a la lista
            lista_personas.append(person)

        return lista_personas
   
    @classmethod
    def filtrar_df(cls, df_persona, id=None, FullName = None, yearOfBirth = None, Gender = None, ZipCode = None):
        queryText=''

        if id!=None:
            queryText+='id=='+ str(id) + ' and '

        if FullName!=None:
            queryText+='FullName.str.contains("' + FullName + '", case=False)'+ ' and '

        if yearOfBirth!=None:
            queryText+='DateNorm >= "' + str(yearOfBirth) + ' and '
            
        if Gender!=None:
            queryText+='Gender.str.contains("' + Gender + '", case=False)'+ ' and '
            
        if ZipCode!=None:
            queryText+='ZipCode.str.contains("' + ZipCode + '", case=False)'+ ' and '
        
        
       #Se castea a todo menos los ultimos 5 caracteres ya que son un " and " adicional con el que siempre termina la query
        return df_persona.query(queryText[:-5], engine="python")
   
    @classmethod
    def get_from_df(cls, df_persona, id=None, FullName = None, yearOfBirth = None, Gender = None, ZipCode = None):
    
        filtro=cls.filtrar_df(df_persona, id=id, FullName=FullName, yearOfBirth=yearOfBirth, Gender=Gender, ZipCode=ZipCode)
        return cls.ConvertirAPersonas(df_persona=filtro)

   
    @classmethod
    def get_stats(cls,df_persona, yearOfBirth = None, Gender = None):
        # Este class method imprime una serie de estadísticas calculadas sobre
        # los resultados de una consulta al DataFrame df_persona. 
        # Las estadísticas se realizarán sobre las filas que cumplan con los requisitos de:
        # yearOfBirth: [yearOfBirth]
        # Gender: [Gender]
        # Las estadísticas son:
        filtro = cls.filtrar_df(df_persona, yearOfBirth = yearOfBirth, Gender= Gender)

        #Cuanto es el total de personas
        #id_max = filtro['id'].max()
        
        # opcion b --> TotalPersonas=len(df_persona)
        TotalPersonas = df_persona['id'].nunique()
        print("El Total de Personas es: ",TotalPersonas)
        
        #TotalFemenino=filtro[filtro['Gender'] == 'F']
        #TotalMasculino=filtro[filtro['Gender'] == 'M']
        #Total por genero        
        TotalFemenino=df_persona['F'].value_counts()
        TotalMasculino=df_persona['M'].value_counts()
        print("La cantidad de Personas Femeninas es : ",TotalFemenino)
        print("La cantidad de Personas Masculinas es : ",TotalMasculino)
        print("El pocentaje de Personas Femeninas es : ",TotalFemenino*100/TotalPersonas)
        print("El pocentaje de Personas Femeninas es : ",TotalFemenino*100/TotalPersonas)
    
        #Obtener un array con los diferentes años en que nacieron las personas
        CantidadAnios=df_persona['Release Date'].nunique()
        print(CantidadAnios)

        #Funcion que convierte el array en una lista
        listaanios=CantidadAnios.tolist()
        
        #For que recorre la lista de los diferentes años en que nacieron las personas
        for n in listaanios:
            count=0
            #For que cuenta cuantas personas nacieron por año
            for j in df_persona['year of birth']:
                if j==n:
                    count=count+1
        print("Para el año ",n," hay ",count," personas")
        