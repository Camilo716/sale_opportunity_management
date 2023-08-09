====================================
Sale Opportunity Management Scenario
====================================


Imports::

    >>> from proteus import Model, Wizard
    >>> from trytond.tests.tools import activate_modules
    >>> from datetime import date, timedelta
    >>> import xml.etree.ElementTree as ET

Activate modules::

    >>> config = activate_modules('sale_opportunity_management')


**Cada sección contiene:**

1. Encabezado, historia de usuario
2. Elementos textuales de propuesta final
3. Descripción detallada
4. Escenarios de pruebas

(Entre [""] estarán los elementos textuales que se acordaron con el cliente en la propuesta final)

----------------------
Registro de prospectos
----------------------
**Como administrador quiero registrar un prospecto para lugo poder hacerle un seguimiento**

["Crear un Formulario de registro rápido de prospecto, Nombres, Métodos de contacto,Direcciones"]


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
    >>> contact_method = prospect.contact_methods.new(contact_type='mobile', value='31223425234', name='Roberto', position='Gerente R.H') 
    >>> contact_method = prospect.contact_methods.new(contact_type='mail', value='peralto@guchitos.org', name='Peralto', position='Administrador') 

    .. >>> Department = Model.get('sale.department')
    .. >>> cundinamarca, = Department.find([('code', '=', 'CO-25')])
    .. >>> prospect.department = cundinamarca

    >>> City = Model.get('sale.city')
    >>> medellin, = City.find([('code', '=', 'CO-05001')])
    >>> prospect.city = medellin
    >>> prospect.save()

Verificar estado final de creación de prospecto::
    >>> prospect.contact_methods 
    [proteus.Model.get('prospect.contact_method')(1), proteus.Model.get('prospect.contact_method')(2)]
    >>> prospect.contact_methods[0].contact_type
    'mobile'
    >>> prospect.contact_methods[0].position
    'Gerente R.H'
    >>> prospect.contact_methods[1].name
    'Peralto'
    >>> prospect.contact_methods[1].value
    'peralto@guchitos.org'

    >>> prospect.city.code
    'CO-05001'
    >>> prospect.department.code
    'CO-05'





------------------------------------
Asignación de prospectos a operarios
------------------------------------
**Como administrador, quiero poder asignar diferentes seguimientos de prospectos a diferentes operarios, para dividir el trabajo de una manera efectiva y que cada operario tenga sus propias llamadas y que no se mezcle con las de los demás**

TODO



-----------------------
Seguimiento de llamadas
-----------------------
**Como operador quiero poder crear un seguimiento de prospecto para luego hacer una llamada**
**Como operador quiero registrar una llamada para luego generar reportes**
**Como operador quiero programar una llamada para luego obtener un reporte de trabajo pendiente**

["Crear Campo para registro de la fecha de la llamada"]

["Crear campo de evento de la llamada con primera llamada, segunda llamada"]

["Crear Campo llamado potencial en el que se asigne un nivel de interés por parte del prospecto identificado en la llamada realizada"]

["Crear campo para asignar descripción ó notas importantes evidenciadas en la llamada"]


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

**Seguimiento de prospecto**:
    * Razon social del prospecto (Tercero)
    * Metodo de contacto del prospecto
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
            
    * Seguimiento de prospecto al que pertence


Crear seguimiento de prospecto::
    >>> ProspectTrace = Model.get('sale.prospect_trace')
    >>> prospect_trace = ProspectTrace()

    >>> prospect_trace.prospect = prospect
    >>> prospect_trace.save()

    >>> prospect_trace.prospect.name
    'guchito S.A.S'
    >>> prospect_trace.prospect_city.name
    'Medellín'
    >>> prospect_trace.prospect_contact.value
    '31223425234'
    >>> prospect_trace.prospect_contact.contact_type
    'mobile'

Crear llamadas a un seguimiento de prospecto desde el seguimiento de prospecto::
    >>> call1 = prospect_trace.calls.new(description='First call', interest='0')
    >>> call2 = prospect_trace.calls.new(description='Second call', interest='1')
    >>> call3 = prospect_trace.calls.new(description='Third call', interest='3')
    >>> prospect_trace.save()

Verificar estado final del seguimiento del prospecto y sus llamadas
    >>> prospect_trace.calls[0].call_result
    'missed_call'
    >>> prospect_trace.calls[0].call_type
    'first_call'
    >>> prospect_trace.calls[0].date == date.today()
    True

    >>> prospect_trace.calls[1].call_result
    'answered_call'
    >>> prospect_trace.calls[1].call_type
    'followup_call'
    
    >>> prospect_trace.calls
    [proteus.Model.get('sale.call')(1), proteus.Model.get('sale.call')(2), proteus.Model.get('sale.call')(3)]
    >>> prospect_trace.current_interest
    '3'
    >>> prospect_trace.state 
    'open'

Programar una próxima llamada pendiente al seguimiento de prospecto::
    >>> pending_call1 = prospect_trace.pending_calls.new(date = date.today() + timedelta(days=7))
    >>> prospect_trace.save()

    >>> prospect_trace.pending_calls
    [proteus.Model.get('sale.pending_call')(1)]

    >>> prospect_trace.state
    'with_pending_calls'


--------
Reportes
--------
["Crear un reporte en el que evidencie por operario y consolidado"]
["Cantidad de llamadas realizadas en un período de tiempo"]
["Crear un reporte para verificar cantidad de llamadas por realizar"]
["Crear reporte para identificación de clientes potenciales (Cliente que en la llamada fueron marcados con un nivel alto)"]


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