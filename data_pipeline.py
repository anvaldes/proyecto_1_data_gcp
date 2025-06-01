import pandas as pd
from sklearn.model_selection import train_test_split
from preprocessing import *

def run_data_pipeline(df):
    """
    Ejecuta el procesamiento y partición del dataset.
    Recibe un DataFrame, retorna un diccionario con los splits procesados.
    """

    # Columnas
    cat_str = ['person_home_ownership', 'loan_intent']
    cat_oh = ['cb_person_default_on_file', 'loan_grade']
    num_mean = ['person_age', 'person_income', 'loan_percent_income']
    num_mean_nan = ['loan_int_rate', 'person_emp_length']
    num_zero_nan = ['loan_amnt']
    X_cols = cat_str + cat_oh + num_mean + num_mean_nan + num_zero_nan
    label = 'loan_status'

    # Filtrado
    df = df[df[label].notna()]

    # Diccionario de transformación
    features_dict = {
        'cat_str': cat_str,
        'cat_oh': cat_oh,
        'num_mean': num_mean,
        'num_mean_nan': num_mean_nan,
        'num_zero_nan': num_zero_nan
    }

    X = df[X_cols].copy()
    y = df[label].copy()

    # Splits
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.40, random_state=10)
    X_val, X_test, y_val, y_test = train_test_split(X_val, y_val, test_size=0.50, random_state=10)

    # Transformaciones
    transformers_pre = get_fit_transfomers(features_dict, X_train, y_train)

    y_train = y_train.reset_index(drop=True)
    y_val = y_val.reset_index(drop=True)
    y_test = y_test.reset_index(drop=True)

    X_train = transform_datasets(transformers_pre, features_dict, X_train)
    X_val = transform_datasets(transformers_pre, features_dict, X_val)
    X_test = transform_datasets(transformers_pre, features_dict, X_test)

    # Retornar datasets procesados como dict
    return {
        'X_train': X_train,
        'y_train': y_train,
        'X_val': X_val,
        'y_val': y_val,
        'X_test': X_test,
        'y_test': y_test,
    }