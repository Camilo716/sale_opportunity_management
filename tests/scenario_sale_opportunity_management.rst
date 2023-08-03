====================================
Sale Opportunity Management Scenario
====================================

Imports::

    >>> from proteus import Model, Wizard
    >>> from trytond.tests.tools import activate_modules
    >>> from datetime import date

Activate modules::

    >>> config = activate_modules('sale_opportunity_management')

----------------------
Registro de prospectos
----------------------
**Como administrador quiero registrar un prospecto para lugo poder hacerle un seguimiento**

El administrador deberá poder registrar los contactos de diferentes prospectos, junto con  su información básica:
    * Razón social (Nombre de la empresa)
    * Ciudad
    * Metodos de contacto
    * Tercero relacionado
        * Nombre
        * Cargo

Crear prospecto::
    >>> Prospect = Model.get('sale.prospect')
    >>> prospect = Prospect()

    >>> prospect.name = 'guchito S.A.S'
    >>> prospect.city = 'Bogotá'
    >>> phone = prospect.contact_methods.new()
    >>> phone.contact_type = 'mobile'
    >>> phone.value = '3132923938'
    >>> prospect.save()

------------------------------------
Asignación de prospectos a operarios
------------------------------------
TODO



-----------------------
Seguimiento de llamadas
-----------------------
**Como operador quiero poder crear un seguimiento de prospecto para luego hacer una llamada**
**Como operador quiero registrar una llamada para luego generar reportes**

El seguimiento de llamadas consiste en realizar llamadas a diferentes contactos con el fin de realizar ofertas de servicios o productos, los cuales pertenecen principalmente a 3 unidades de negocio:
    * Optica
    * Brigada
    * Equipos

Luego de realizar estas llamadas, el operador dejará registro sobre aspectos como el interés del prospecto, descripción u observaciones importantes, tipificación del prospecto...

Cada conjunto de **llamadas** a un prospecto, se llamará **seguimiento de prospecto**, por lo que este podrá tener varias llamadas, y una llamada solo podrá  pertenecer a un seguimiento de prospecto. Ej:

Seguimiento de prospecto 1
    * llamada 1
    * llamada 2

Seguimiento de prospecto 2
    * llamada 1
    * llamada 2
    * llamada 3


Crear seguimiento de prospecto::
    >>> ProspectTrace = Model.get('sale.prospect_trace')
    >>> prospect_trace = ProspectTrace()

    >>> prospect_trace.prospect = prospect
    >>> prospect_trace.save()

    >>> prospect_trace.prospect_name
    'guchito S.A.S'
    >>> prospect_trace.prospect_city
    'Bogotá'


Crear llamada a un seguimiento de prospecto::
    >>> Call = Model.get('sale.call')
    >>> call = Call()

    >>> call.description = 'Descripción u observaciones de la llamada'
    >>> call.prospect_trace = prospect_trace
    >>> call.save()

    >>> call.prospect_trace.prospect_name
    'guchito S.A.S'
    >>> call.date == date.today()
    True

Crear otra llamada al mismo seguimiento de prospecto::
    >>> Call = Model.get('sale.call')
    >>> call = Call()

    >>> call.description = 'Segunda llamada al mismo seguimiento'
    >>> call.prospect_trace = prospect_trace
    >>> call.save()

    >>> call.prospect_trace.prospect_name
    'guchito S.A.S'
    >>> call.prospect_trace.prospect_city 
    'Bogotá'
    >>> call.date == date.today()
    True
    >>> len(prospect_trace.calls) == 2
    True

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
    * Seguimiento de prospecto al que pertenecen las llamadas