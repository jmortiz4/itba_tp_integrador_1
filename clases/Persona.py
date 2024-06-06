import pandas as pd
import sys
sys.path.append('../')
import Helper as faux


# Personas: Cantidad de personas por año de nacimiento y Género. Cantidad total de personas.
class Persona:
    def __init__(self, fullname, yearOfBirth, gender , zipcode, id=None):
        self.id = id
        self.fullName = fullname
        self.yearOfBirth =yearOfBirth
        self.gender = "-" if gender == None else gender
        self.zipcode = zipcode
        
    def __repr__(self):
        # Este método debe imprimir la información de esta persona.
        return f'\n [{self.id}] {self.fullName} ({self.yearOfBirth}) -{self.gender.replace("M","Masculino").replace("F","Femenino")}- CP:{self.zipcode} ' 
    
    def write_df(self, df):
        
        df_persona = df.copy()
        if self.id == None:
            self.id=df_persona['id'].max()+1
        elif self.id in df_persona['id']:
            print('Error: No se pudo agregar, id ya existente')
            return df_persona
            
        new_row = {'id':self.id,'Full_Name': self.fullName, 'year_of_birth' : self.yearOfBirth, 'Gender' : self.gender, 'Zip_Code' : self.zipcode }
        df_persona.loc[self.id] = new_row

            
        return df_persona
        
    def remove_from_df(self, df):
        # Borra del DataFrame el objeto contenido en esta clase.
        # Para realizar el borrado todas las propiedades del objeto deben coincidir
        # con la entrada en el DF. Caso contrario imprime un error.
        df_persona= df.copy()
        
        fila_a_borrar=self.filtrar_df(df_persona, id=self.id, FullName = self.fullName, yearOfBirth = self.yearOfBirth, Gender = self.gender, ZipCode = self.zipcode)
        if len(fila_a_borrar)==1:
            return df_persona.drop(fila_a_borrar.index)

        else:
            print("No existe en el df recibido una persona exactamente igual a la que invoca esta acción")
            return df_persona

    @classmethod
    def create_df_from_csv(cls, file_personas):
       
        df_personas = pd.read_csv(file_personas) 
        df_personas=faux.reemplazo_espacios_por_guion_bajo(df_personas)
  
        return df_personas
    
    @classmethod
    def ConvertirAPersonas(cls,df_persona):
        # Este class method recibe un df y devuelve un listado de personas
        lista_personas = []
        # Itera sobre cada fila del DataFrame
        for index, row in df_persona.iterrows():
            # Crea un objeto Persona con los datos de la fila actual
            FullName=row['Full_Name']
            yearOfBirth=row['year_of_birth'] 
            Gender=row['Gender']
            ZipCode=row['Zip_Code']
            id=row['id']
            person = Persona(fullname=FullName, yearOfBirth=yearOfBirth, gender=Gender , zipcode=ZipCode, id=id)
            lista_personas.append(person)

        return lista_personas
   
    @classmethod
    def filtrar_df(cls, df_persona, id=None, FullName = None, yearOfBirth = None, Gender = None, ZipCode = None):
        queryText=''

        if id!=None:
            queryText+='id=='+ str(id) + ' and '

        if FullName!=None:
            queryText+='Full_Name.str.contains("' + FullName + '", case=False)'+ ' and '

        if yearOfBirth!=None:
            if isinstance(yearOfBirth,int):
                desde=yearOfBirth
                hasta=yearOfBirth
            else:
                desde,hasta=yearOfBirth
            queryText+='year_of_birth >= '+str(desde)+' and year_of_birth <= '+str(hasta)+' and '
            
        if Gender!=None:
            queryText+='Gender == \'' + Gender + '\' and '
            
        if ZipCode!=None:
            queryText+='Zip_Code == \'' + ZipCode + '\' and '
        
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
        TotalPersonas=filtro.shape[0]
        filtroAgrupado = filtro.groupby(['year_of_birth', 'Gender']).size().unstack(fill_value=0)
        print("El Total de Personas es: ",TotalPersonas)
        if Gender!='M':
            TotalFemenino=filtroAgrupado['F'].sum()
            print(f'Femeninas: {TotalFemenino} ({round((TotalFemenino*100/TotalPersonas),1)}%)')

        if Gender!='F':
            TotalMasculino=filtroAgrupado['M'].sum()
            print(f'Masculinos: {TotalMasculino} ({round((TotalMasculino*100/TotalPersonas),1)}%)')
        
        faux.plot_lineas_genero_añoNacimiento(filtroAgrupado)
    
        