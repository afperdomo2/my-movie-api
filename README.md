### Configuración

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
```

### Proyecto

`--reload`: Esto le dice a Uvicorn que reinicie el servidor cada vez que detecte un cambio en los archivos de origen.

`--port 3500`: Esto le dice a Uvicorn que escuche en el puerto 3500 en lugar del puerto predeterminado, que es 8000.

`--host 0.0.0.0`: Esto le dice a Uvicorn que escuche en todas las interfaces de red disponibles. Por defecto, Uvicorn solo escucha en localhost (127.0.0.1), lo que significa que solo se puede acceder al servidor desde la misma máquina. Al escuchar en 0.0.0.0, el servidor puede ser accedido desde cualquier máquina que pueda llegar a tu máquina a través de la red.

```sh
# Ejecutar el proyecto
uvicorn main:app --reload
uvicorn main:app --reload --port 3500
uvicorn main:app --reload --port 3500 --host 0.0.0.0
```
