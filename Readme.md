# Descripción

Clase para recuperar y respaldar la configuración de un proyecto que ha establecido un usuario.

El fichero de configuración se espera que este en formato `json`.

Por defecto el fichero de configuración se denomina como `config.json` y se almacena en una subcarpeta dentro de la carpeta home del usuario. La ruta completa se calcula con el home del usuario, la subcarpeta definida con la constante `FOLDER_PROJECTS` que tiene el valor por defecto `'.nk'` y por último el nombre del proyecto.

Por ejemplo, para un proyecto que se llame `test`, la ruta sería:

```bash
~/.nk/test/config.json
```

Si la carpeta no existiese se crearía.

Si el fichero de configuración no existiese, se busca dentro de la carpeta del proyecto un archivo local de configuración para cargar los valores por defecto de configuración. En caso contrario se mostrará un error fatal.

## Dependencias

Depende del modulo `msgterm`, que deberá estar presente en el proyecto.