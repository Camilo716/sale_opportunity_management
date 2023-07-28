=====================================
Gestión de oportunidades por llamadas
=====================================

----------------------
Registro de prospectos
----------------------

El administrador deberá poder registrar los contactos de diferentes prospectos, junto con  su información básica:
    * Razón social (Nombre de la empresa)
    * Ciudad
    * Metodos de contacto
    * Tercero relacionado
        * Nombre
        * Cargo

------------------------------------
Asignación de prospectos a operarios
------------------------------------

.. TODO

-----------------------
Seguimiento de llamadas
-----------------------

El seguimiento de llamadas consiste en realizar llamadas a diferentes contactos con el fin de realizar ofertas de servicios o productos, los cuales pertenecen principalmente a 3 unidades de negocio:
    * Optica
    * Brigada
    * Equipos

Luego de realizar estas llamadas, el operador dejará registro sobre aspectos como el interés del cliente, descripción u observaciones importantes, tipificación del cliente...

Cada conjunto de **llamadas** a un cliente, se llamará **seguimiento de cliente**, por lo que este podrá tener varias llamadas, y una llamada solo podrá  pertenecer a un seguimiento de cliente. Ej:

Seguimiento de cliente 1
    * llamada 1
    * llamada 2

Seguimiento de cliente 2
    * llamada 1
    * llamada 2
    * llamada 3

**Seguimiento de cliente**:
    * Razon social del cliente (Tercero)
    * Metodo de contacto del cliente
    * Unidad de negocio
    * Estado (Abierto o cerrado)
    * Llamadas

**LLamada**:
    * Fecha
    * Descripion o observaciones
    * Nivel de interés (0-3)
        * 0 - No contestó
        * 1 - total desinterés
        * 2 - Interés intermedio, brindar mas información
        * 3 - Interés alto, generar venta
    
    * Estado (realizada - pendiente)
    * Seguimiento de cliente al que pertence

--------
Reportes
--------
* Reporte de llamadas realizadas en un periodo de tiempo (Análisis de operarios):
    * Nivel de interés
    * Unidad de negocio
    * Observaciones
    * Operario

* Reporte de seguimientos a prospectos (Análisis de prospectos):
    * Interés durante distintas etapas del seguimiento


* Reporte de Llamadas a realizar (Analisis de trabajo pendiente):
    * Llamadas pendientes
    * Seguimientos a prospectos abiertos

* Reporte de seguimientos sin asignar - asignados:
    * Seguimientos a prospectos pendientes por asignar a operador

* Reporte de prospectos potenciales
    * llamadas con un nivel de interés alto
    * Seguimiento de cliente al que pertenecen las llamadas
