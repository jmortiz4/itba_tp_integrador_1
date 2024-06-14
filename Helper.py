import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import sys
sys.path.append('../') 
from clases.Scores import Score
from clases.Peliculas import Pelicula
from clases.Usuario import Usuario
from clases.Trabajador import Trabajador
from clases.Persona import Persona


def load_all(file_personas, file_trabajadores, file_usuarios, file_peliculas, file_scores):
    
    df_peliculas =Pelicula.create_df_from_csv(file_peliculas)
    df_personas = Persona.create_df_from_csv(file_personas)
    df_usuarios = Usuario.create_df_from_csv(file_usuarios)
    df_trabajadores= Trabajador.create_df_from_csv(file_trabajadores)
    df_scores = Score.create_df_from_csv(file_scores)

    return df_personas, df_trabajadores, df_usuarios, df_peliculas, df_scores
    

def save_all(df_personas, df_trabajadores, df_usuarios, df_peliculas, df_scores,
              file_personas="personas.csv", file_trabajadores="trabajadores.csv",
                file_usuarios="usuarios.csv", file_peliculas="peliculas.csv", file_scores="scores.csv"):
    #Código de Salvado
    return 0 # O -1 si hubo algún error 

def reemplazo_espacios_por_guion_bajo(df):
    df.columns = [col.replace(' ', '_') for col in df.columns]
    return df


def eliminoCaracterDeColumnasDF(df,caracteres):

    #Elimino lss caracteres deseados simples de los headers ya que luego traen problemas con el df.query

    for car in caracteres:

        columns_with_special_chars = [col for col in df.columns if car in col]
        cambios = {x : x.replace(car,"") for x in columns_with_special_chars}
        df.rename(columns=cambios, inplace=True)

    return df

def elminoCaracterDeLista(lista,caracteres):
    listaOK=lista.copy()
    for car in caracteres:
        listaOK=[x.replace(car,"") for x in listaOK]
    return listaOK


def trasladar_rating_a_columnas_generos(row, merged_df):

    for column in merged_df.columns[3:]:
        if merged_df.at[row.name, column] == 1:
            merged_df.at[row.name, column] = row['rating']
        elif merged_df.at[row.name, column] == 0:
            merged_df.at[row.name, column] = np.nan

def plot_lineas_rating_añoPelicula_generos(dfPlot,dfPlotInterpolado, generosDeseadosList):
    # Configurar el gráfico
    base_color = list(mcolors.BASE_COLORS.values())
    plt.figure(figsize=(10, 6))
    counter=0
    # Trazar las líneas
    for genero in generosDeseadosList:
        counter+=1
        plt.plot(dfPlotInterpolado['year'], dfPlotInterpolado[genero], marker='_', color=base_color[counter],label=genero)
        plt.scatter(dfPlot['year'], dfPlot[genero], color=base_color[counter])
  

    # Etiquetas y título
    plt.xlabel('Año')
    plt.ylabel('Puntuación Promedio')
    plt.title('Puntuación Promedio por Año Según Generos')
    plt.legend()

    # Mostrar el gráfico
    plt.grid(True)
    return plt


def barplot_cantdad_año_generos(tabla):

    # Crear el gráfico de barras apiladas
    grafico = tabla.plot(kind='bar', stacked=True, figsize=(10, 7))

    # Configurar las etiquetas y el título
    plt.xlabel('Year')
    plt.xticks(rotation=45)

    plt.ylabel('Number of Movies')
    max_y = tabla.sum(axis=1).max() # Calcular el valor máximo del eje y
    plt.yticks(range(0, int(max_y) + 1, 2))  # Define los saltos discretos desde 0 hasta el valor máximo calculado

    plt.title('Number of Movies per Genre by Year', fontsize=20)  # Ajustar el tamaño del título
    plt.legend(title='Genre', loc='upper left')  # Ubicar la leyenda arriba a la izquierda

    # Agregar etiquetas de datos dentro de las cajas
    for container in grafico.containers:
        for bar in container:
            height = bar.get_height()
            width = bar.get_width()
            x, y = bar.get_xy()
            grafico.text(x + width / 2, y + height / 2, f'{height:.0f}', ha='center', va='center')

    plt.show()


def barplot_comparativo_edad_genero_rating(df):

    # Crear bins de 5 años para las edades
    colors = {'F': 'salmon', 'M': 'turquoise'}
    bins = range(df['age'].min(), df['age'].max(), 5)  # Ajustar según el rango de edades en los datos
    labels = [f'{i}-{i+4}' for i in bins[:-1]]
    df['age_bin'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

    # Calcular el promedio de calificaciones por bin de edad y género
    average_ratings = df.groupby(['age_bin', 'Gender'])['rating'].mean().reset_index()


    # Crear un gráfico de barras comparativas
    plt.figure(figsize=(14, 7))
    sns.barplot(data=average_ratings, x='age_bin', y='rating', palette=colors,hue='Gender')
    plt.title('Puntuación promedio por Rango Etario comparando Generos')
    plt.xlabel('Rango Etario')
    plt.ylabel('Promedio Puntuación')
    plt.legend(title='Genero')
    plt.grid(True)

    plt.show()

def kdeplot_edad_genero_rating(df):
    # Crear gráficos de distribución separados por género
    plt.figure(figsize=(14, 6))

    # Gráfico para género masculino
    plt.subplot(1, 2, 1)
    sns.kdeplot(x='age', y='rating', data=df[df['Gender'] == 'M'], fill=True, cmap='Blues', alpha=0.6)
    plt.title('Distribution Plot for Males')
    plt.xlabel('Age')
    plt.ylabel('Rating')
    plt.xlim(30, 100)
    plt.xticks(range(30, 101, 10))  
    plt.ylim(1, 5)
    

    # Gráfico para género femenino
    plt.subplot(1, 2, 2)
    sns.kdeplot(x='age', y='rating', data=df[df['Gender'] == 'F'], fill=True, cmap='Reds', alpha=0.6)
    plt.title('Distribution Plot for Females')
    plt.xlabel('Age')
    plt.ylabel('Rating')
    plt.xlim(30, 100)
    plt.xticks(range(30, 101, 10))  
    plt.ylim(1, 5)
    

    plt.tight_layout()
    plt.show()

def HorizontalBarplot_usuario_rating(df):
    # Crear un gráfico de barras horizontales comparativas con la paleta 'pastel'
        df['ocupacion'] = df['ocupacion'].str.capitalize()
        plt.figure(figsize=(10, 7))
        sns.barplot(data=df, y='ocupacion', x='rating', orient='h')
        plt.title('Puntuacion promedio por profesión')
        plt.ylabel('Ocupacion')
        plt.xlabel('Puntuacion promedio')
        plt.grid(True)
        plt.show()


def plot_lineas_genero_añoNacimiento(df):

    # Graficar los datos
    # Colores para cada género
    colors = {'M': 'blue', 'F': 'red'}

    # Graficar cada género por separado
    plt.figure(figsize=(10, 6))
    for gender in df.columns:
        plt.plot(df.index, df[gender], marker='o', color=colors[gender], label='Masculino' if gender == 'M' else 'Femenino')

       # Configurar el título y etiquetas de los ejes
    
    plt.title('Personas por género agrupados por año de nacimiento')
    plt.xlabel('Año de Nacimiento')
    plt.ylabel('Personas')
    plt.grid(True)
    plt.legend(title='Género')

    # Mostrar el gráfico
    plt.show()


def heatmap_ocupacion_nacimiento(grouped_data):
    # Crear el mapa de calor
    plt.figure(figsize=(12, 8))
    pivot_table = grouped_data.pivot( "ocupacion", "year_of_birth","count")
    sns.heatmap(pivot_table,cmap="crest")
    plt.title("Mapa de Calor de Ocupaciones por Año de Nacimiento")
    plt.xlabel("Año de Nacimiento")
    plt.yticks(rotation=0)
    plt.xticks(rotation=90)
    plt.ylabel("Ocupación")
    return plt.show()

def barplot_puestos_nacimiento(tabla):
    # Crear el gráfico de barras
    plt.figure(figsize=(12, 8))
    for position in tabla['Position'].unique():
        data = tabla[tabla['Position'] == position]
        plt.bar(data['year_of_birth'], data['count'], label=position)
    
    # Configuración del gráfico
    plt.xlabel('Año de Nacimiento')
    plt.ylabel('Número de Puestos')
    plt.title('Número de Puestos de Trabajadores por Año de Nacimiento')
    plt.xticks(rotation=45)
    plt.legend(title='Position', loc='upper left')

    # Mostrar el gráfico
    plt.tight_layout()
    plt.show()