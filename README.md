# Proyecto de Desarrollo - Sistemas Distribuidos

Proyecto de desarrollo para la materia **Desarrollo de Software en Sistemas Distribuidos**.

---

## Backend

Para trabajar con el backend se usan dos comandos principales:

1. `poetry install`

   - Instala todas las dependencias del proyecto según `pyproject.toml`.
   - Crea y usa un entorno virtual gestionado por Poetry para que las librerías queden aisladas del sistema.

2. `flask run`
   - Inicia el servidor de desarrollo de Flask.
   - Permite ejecutar la aplicación localmente y acceder a la API en `http://localhost:5000` por defecto.

> 💡 Orden recomendado: primero ejecutar `poetry install` para instalar dependencias, luego `flask run` para levantar la aplicación.
