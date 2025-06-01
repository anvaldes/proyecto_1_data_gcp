import pandas as pd

def uniendo_data(dataframes):
    """
    Une una lista de DataFrames por columnas (axis=1).
    Retorna un único DataFrame combinado.
    """
    df = pd.concat(dataframes, axis=0)
    print(f'Unidos {len(dataframes)} archivos en memoria. Shape final: {df.shape}')
    return df
