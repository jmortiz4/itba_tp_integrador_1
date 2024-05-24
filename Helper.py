import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def load(file):
    return pd.read_csv(file)

def load_all(file_personas='personas.csv', file_trabajadores='trabajadores.csv', file_usuarios='usuarios.csv', file_peliculas='peliculas.csv', file_scores='scores.csv'):
    
    df_peliculas =load(file_peliculas)
    df_personas = load(file_personas)
    df_usuarios = load(file_usuarios)
    df_trabajadores= load(file_trabajadores)
    df_scores = load(file_scores)

    return df_personas, df_trabajadores, df_usuarios, df_peliculas, df_scores


def save_all(df_personas, df_trabajadores, df_usuarios, df_peliculas, df_scores,
              file_personas="personas.csv", file_trabajadores="trabajadores.csv",
                file_usuarios="usuarios.csv", file_peliculas="peliculas.csv", file_scores="scores.csv"):
    #Código de Salvado
    return 0 # O -1 si hubo algún error 


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