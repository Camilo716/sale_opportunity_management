=====================================
Gestión de oportunidades por llamadas
=====================================

--------------------
Registro de clientes
--------------------

El administrador deberá poder registrar los contactos de diferentes clientes, junto con  su información básica:
    * Razón social (Nombre de la empresa)
    * Ciudad
    * Metodos de contacto
    * Tercero relacionado
        * Nombre
        * Cargo

----------------------------------
Asignación de clientes a operarios
----------------------------------

.. TODO

-----------------------
Seguimiento de llamadas
-----------------------

El seguimiento de llamadas consiste en realizar llamadas a diferentes contactos con el fin de realizar ofertas de servicios o productos, los cuales pertenecen principalmente a 3 unidades de negocio:
    * Optica
    * Brigada
    * Equipos

Luego de realizar estas llamadas, el operador dejará un registro sobre aspectos como el interés del cliente, descripción o observaciones importantes, tipificación del cliente...

Cada conjunto de **llamadas** a un cliente, se llamará **seguimiento de cliente**, por lo que
este podrá tener varias llamadas, y una llamada solo podrá  pertenecer a un seguimiento
de cliente. Ej:

Seguimiento de cliente 1
    * llamada 1
    * llamada 2

Seguimiento de cliente 2
    * llamada 1
    * llamada 2
    * llamada 3

**Seguimiento**:
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

--------
Reportes
--------

Reportes a realizar:
    * Llamadas realizadas en un periodo de tiempo:
        * Nivel de interés
        * Unidad de negocio
        * Observaciones

    * Llamadas a realizar (Pendientes)
    * Tercero sin asignar - Asignados

.. TODO
