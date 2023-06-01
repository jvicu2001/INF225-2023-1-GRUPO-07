# Cómo inicializar servicios de Hito 4

## Servicio Metadatos
- Vamos al directorio del servicio
> cd metadata/api

- Inicializamos un entorno virtual (1ra vez)
> python3 -m venv .venv

- Inicializamos un entorno virtual (1ra vez) e ingresamos al entorno virtual
    - Linux:
    > python3 -m venv .venv

    > source .venv/bin/activate

    - Windows:
    > python -m venv .venv

    > .venv/Scripts/activate.bat

- Volvemos a la carpeta raiz del proyecto

- Ejecutamos el servicio
> uvicorn metadata.api.app:app --restart --port 8001

---
## Servicio Almacenamiento
- Vamos al directorio del servicio
> cd storage/api

- Inicializamos un entorno virtual (1ra vez) e ingresamos al entorno virtual
    - Linux:
    > python3 -m venv .venv

    > source .venv/bin/activate

    - Windows:
    > python -m venv .venv

    > .venv/Scripts/activate.bat

- Volvemos a la carpeta raiz del proyecto

- Ejecutamos el servicio
> uvicorn storage.api.main:app --restart --port 8000