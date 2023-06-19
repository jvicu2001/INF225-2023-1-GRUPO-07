FROM python:3.11.4-slim-bookworm

WORKDIR /opt/app

COPY . .

# Descargar requerimientos
RUN pip install -r api/requirements.txt

# Ejecutar API
ENTRYPOINT [ "python3" , "api/main.py" ]