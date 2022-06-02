# Creando App Core

La aplicación Core de nuestro proyecto se va a encargar de conectar la lógica entre otras aplicaciones, además de que las migraciones y las bases de datos se manejan mejor desde dicha aplicación. Ejecutamos el siguiente comando:

```txt
python manage.py startapp core
```

El desarrollo de este proyecto está guiado por pruebas, aplicando la metodología TDD (Test-Driven Development - Desarrollo dirigido por pruebas), pero por el momento, el archivo `tests.py` no lo vamos a usar dentro de está aplicación `core`, por lo tanto lo eliminamos. Hacemos lo mismo para el archivo `views.py`.

Vamos a crear un nuevo folder llamado `core/test`, en el cuál escribiremos los test de nuestros modelos. Dentro de dicho folder creamos un archivo `__init__.py`

| Anterior |                           | Siguiente                                  |
| -------- | ------------------------- | ------------------------------------------ |
| [Instalando Paquetes y Creación del Proyecto](01_Instalando_Paquetes_Creacion_Proyecto.md) | [Readme](../../README.md) | [Test para Modelo de Usuario Personalizado](03_Test_Modelo_Usuario_Personalizado.md) |
