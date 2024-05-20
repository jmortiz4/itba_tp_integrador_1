import pandas as pd

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