# Usa una versión más actual de Python, compatible con tus libs
FROM python:3.10

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia e instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Expone el puerto esperado por Cloud Functions / Cloud Run
ENV PORT=8080

# Comando de entrada para el servidor Flask usando Gunicorn
CMD ["gunicorn", "--bind", ":8080", "main:app"]
