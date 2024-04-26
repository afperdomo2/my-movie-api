# my-movie-api

## 🪛 1. Configuración

```sh
# Crear un entorno virtual en el directorio actual
python -m venv venv

# Activar el entorno virtual (windows)
venv/Scripts/activate

# Salir del entorno virtual
deactivate

# Instalar módulos en el entorno virtual
pip install fastapi
pip install uvicorn

# Muestra una lista de todas las bibliotecas de Python instaladas en el entorno actual
pip freeze > requirements.txt
```

### Proyecto

Se debe de ejecutar los scripts dentro del entorno del proyecto

`--reload`: Esto le dice a Uvicorn que reinicie el servidor cada vez que detecte un cambio en los archivos de origen.

`--port 3500`: Esto le dice a Uvicorn que escuche en el puerto 3500 en lugar del puerto predeterminado, que es 8000.

`--host 0.0.0.0`: Esto le dice a Uvicorn que escuche en todas las interfaces de red disponibles. Por defecto, Uvicorn solo escucha en localhost (127.0.0.1), lo que significa que solo se puede acceder al servidor desde la misma máquina. Al escuchar en 0.0.0.0, el servidor puede ser accedido desde cualquier máquina que pueda llegar a tu máquina a través de la red.

```sh
# Ejecutar el proyecto
uvicorn main:app --reload
uvicorn main:app --reload --port 3500
uvicorn main:app --reload --port 3500 --host 0.0.0.0
```

## 🐳 2. Deploy

Ejecutar el proyecto con Docker y docker-compose

```sh
docker-compose up --build -d
```

## 📚 3. Documentación - swagger

Modificar el host y el puerto según la configuración del proyecto

📺Local:
[http://localhost:3500/docs](http://localhost:3500/docs)

🐳Docker:
[http://localhost:3600/docs](http://localhost:3600/docs)
