from flask import Flask, request
from google.cloud import storage
import pandas as pd
from io import StringIO
from uniendo_data import uniendo_data
from data_pipeline import run_data_pipeline

app = Flask(__name__)

print("✔ Flask app is loading...")

@app.route("/", methods=["GET"])
def pipeline():
    year = request.args.get("year", "2025")
    month = request.args.get("month", "06")
    bucket_name = "proyecto_1_ml"

    client = storage.Client(project="proyecto-1-461620")

    print(f"Iniciando pipeline para {year}-{month}")

    # ------------------------------
    # 1. Descargar archivos desde GCS a memoria
    # ------------------------------
    dfs = []
    for i in range(1, 4):
        blob_path = f"source_data/{year}_{month}/credit_risk_{i}.csv"
        blob = client.bucket(bucket_name).blob(blob_path)
        content = blob.download_as_text()
        df = pd.read_csv(StringIO(content))
        dfs.append(df)

    # ------------------------------
    # 2. Unir los DataFrames
    # ------------------------------
    df_combined = uniendo_data(dfs)
    print(f"Shape después de unir: {df_combined.shape}")

    # ------------------------------
    # 3. Ejecutar pipeline de datos
    # ------------------------------
    outputs = run_data_pipeline(df_combined)
    print("Transformaciones completadas")

    # ------------------------------
    # 4. Subir resultados a GCS
    # ------------------------------
    for name, df in outputs.items():
        csv_data = df.to_csv(index=False)
        blob_path = f"datasets/{year}_{month}/{name}.csv"
        blob = client.bucket(bucket_name).blob(blob_path)
        blob.upload_from_string(csv_data, content_type='text/csv')
        print(f"Subido: {blob_path}")

    return f"YESSS! Pipeline completado y datasets guardados para {year}-{month}", 200