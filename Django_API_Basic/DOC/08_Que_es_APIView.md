# ¿Que es una APIView?

Tenemos 2 maneras de mostrar la información de nuestros modelos en la API:

- APIView
- ViewSet

El APIView presenta un mayor control sobre la lógica, en especial aquella que se considera lógica difícil. También nos permite llamar a otras APIs y trabajar con archivos locales. Usa métodos HTTP standard (`get()`, `post()`)

## ¿Cuando Usar APIViews?

- Si se necesita control de lógica
- Procesamiento de archivos y renderización de respuestas sincronizadas
- Llamado a otras APIs y/o servicios
- Acceso a archivos locales o datos

| Anterior |                        | Siguiente                                   |
| -------- | ---------------------- | ------------------------------------------- |
| [Acceso de Admin](07_Acceso_Admin.md) | [Readme](../README.md) | [Creando primer APIView](09_Creando_Primer_APIView.md) |
