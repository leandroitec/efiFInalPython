# EFI Final Python Integrantes:

. Bressan Nadal Franco Nicolas
<br>
. Leandro Odetto

## INSTRUCCIONES PRIMERA VEZ

    1. Clonar el repositorio
    2. Verificar si esta instalado uv ($ uv --version), si no larga un mensaje con la version debes instalarlo ($ pipx install uv).
    3. Instalar la paqueteria de pyproyect.tolm con (& uv sync).
    4. Verificar en app.py la conexion a la base de datos local. 
    6. Borrar carpeta migratios (si existe)
    7. Iniciar flask db ($ uv run flask db init) SOLO UNA VEZ
    8. Actualizar db ($ uv run flask db migrate)
    9. Aplicar cambios ($ uv run flask db upgrade)
    10 Iniciar servidor (& uv run flask run --reload)
    11. Abrir navegador y acceder a http://127.0.0.1:5000

## COMANDOS

1. Iniciar servidor __uv run flask run --reload__

## ESTRUCTURA

- **efiFInalPython**
    - assets/
    - models/
        - models.py
    - api/
        - schemas.py
        - views.py
    - app.py
    - decorators.py

## ESQUEMA Y RELACIONES BD

![Diagrama de BD](assets/estructura_BD.png)

## COMENTARIOS INTERNOS DEL GRUPO
##### Generales
1. Creo esta seccion para la comunicacion del grupo si fuese necesario (recordar subir el README a main)
2. Cambie la estructrura general del proyecto, ver de pasar los decorator a su propio archivo en carpeta raiz
3. Ahora el codigo esta comentado. __RECORDAR__ pulir el codigo
4. HAY UN PROBLEMA __IMPORTANTE__: en la BD, User tiene "name" pero en UserSchema, tenemos "username". MEJORAR SCHEMA PARA QUE SEA "name" TAMBIEN, O AMBAS, SINO ES CONFUSO.__AHORA__ BD: User.name, Schema: "username"
###### UserDetailAPI
1. Metodos GET, PUT, PATCH funcionales
2. Falta DELETE
3. PUT, Solo se edita username y mail, __FALTA__ pasword, etc.
4. PATCH, funciona, falta pulir
5. HAY UN PROBLEMA __IMPORTANTE__: en la BD, User tiene "name" pero en UserSchema, tenemos "username". MEJORAR SCHEMA PARA QUE SEA "name" TAMBIEN, O AMBAS, SINO ES CONFUSO (pongo esto en general)
## AVANCES/CHECKLIST

- Creo esta seccion para controlar mas adelante que falta de la consigna


