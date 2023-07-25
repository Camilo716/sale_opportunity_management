# CONTRIBUIR

### requerimientos tecnicos

* python >= 3.9
* docker >= 20
* docker-compose >= 2
* pre-commit >= 2
* git >= 2.30
* rake >= 13

### procedimiento

1. iniciar entorno `rake init`
2. iterar con `rake tdd`
3. detener el entorno `rake down`

### consideraciones

* evito trabajo innecesario
* evito generalizar, primero hago pruebas y luego elimino duplicidad
* evito redundancia, si lo puedo automatizar lo automatizo
* evito usar `git add .`
* a todo momento hago expresivo lo escrito, renombro, muevo o elimino
* en todo momento debo poder ejecutar las pruebas
* en todo momento debo poder el programa
* en todo momento especulo, me ilustro y aprendo

### convencion commit

ante cada commit el mensaje se clasifica en:
*  **feat(\<COMPONENTE\>)** una nueva funcionalidad accesible al usuario o sistema
*  **fix(\<COMPONENTE\>)** correcion de una funcionalidad ya entregada
*  **chore(\<COMPONENTE\>)** otros cambios que no impactan directamente al usuario, ejemplo renombramiento de archivo,clases,metodos,variables,carpetas,scripts, documentacion, recursos digitales, etc..

`COMPONENTE` nombre del directorio

ejemplos:

`git commit -m 'feat(<COMPONENTE>): venta de equipos opticos`

`git commit -m 'fix(<COMPONENTE>): se adiciona boton faltante`

`git commit -m 'chore(<COMPONENTE>): cambio de color en columna Producto`
