====================================
Sale Opportunity Management Scenario
====================================


Imports::

    >>> from proteus import Model, Wizard
    >>> from trytond.tests.tools import activate_modules
    >>> from datetime import date, timedelta, datetime
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
    >>> prospect1 = Prospect()
    
    >>> prospect1.name = 'guchito S.A.S'
    >>> contact_method = prospect1.contact_methods.new(value='31223425234', name='Roberto', job='Gerente R.H') 
    >>> contact_method = prospect1.contact_methods.new(contact_type='mobile', value='12345678910', name='Pancracia', job='Asistente administrativo') 
    >>> contact_method = prospect1.contact_methods.new(contact_type='mail', value='peralto@guchitos.org', name='Peralto', job='Administrador')  
    >>> City = Model.get('sale.city')
    >>> medellin, = City.find([('code', '=', 'CO-05001')])
    >>> prospect1.city = medellin
    >>> prospect1.business_unit = 'brigade'
    >>> prospect1.save()

Verificar estado final de creación de prospecto::
    >>> prospect1.contact_methods 
    [proteus.Model.get('prospect.contact_method')(1), proteus.Model.get('prospect.contact_method')(2), proteus.Model.get('prospect.contact_method')(3)]
    >>> prospect1.contact_methods[0].contact_type
    'mobile'
    >>> prospect1.contact_methods[0].job
    'Gerente R.H'
    >>> prospect1.contact_methods[2].name
    'Peralto'
    >>> prospect1.contact_methods[2].value
    'peralto@guchitos.org'

    >>> prospect1.city.code
    'CO-05001'
    >>> prospect1.department.code
    'CO-05'
    >>> prospect1.business_unit
    'brigade'
    >>> prospect1.state
    'unassigned'

Crear segundo prospecto::
    >>> prospect2 = Prospect()
    
    >>> prospect2.name = 'Modernitus S.A.S'
    >>> contact_method = prospect2.contact_methods.new(value='3122390987', name='Pepe', job='Jefe de ventas') 

    >>> City = Model.get('sale.city')
    >>> bogota, = City.find([('code', '=', 'CO-11001')])
    >>> prospect2.city = bogota
    >>> prospect2.business_unit = 'brigade'
    >>> prospect2.save()

Crear tercer prospecto::
    >>> prospect3 = Prospect()
    
    >>> prospect3.name = 'Vision S.A.S'
    >>> contact_method = prospect3.contact_methods.new(value='3122324287', name='Alfredo', job='Administrador') 
    >>> prospect3.business_unit = 'optics'
    >>> prospect3.save()

Asignar tipificación a un prospecto
    >>> prospect3.rating = '1'
    >>> prospect3.comments = 'Calificación al cliente' 

------------------------------------
Asignación de prospectos a operarios
------------------------------------
**Como administrador, quiero poder asignar diferentes seguimientos de prospectos a diferentes operarios, para dividir el trabajo de una manera efectiva y que cada operario tenga sus propias llamadas y que no se mezcle con las de los demás**

Asignar prospectos a un operario::
    >>> User = Model.get('res.user')
    >>> user,  = User.find([('name', '=', 'Administrator')])

    >>> assign = Wizard('sale.prospect.assign', [prospect1, prospect2, prospect3])
    >>> assign.form.business_unit = 'brigade'
    >>> assign.form.prospects_chunk = 3
    >>> assign.form.operator = user
    >>> assign.form.prospects
    [proteus.Model.get('sale.prospect')(1), proteus.Model.get('sale.prospect')(2)]
    >>> assign.execute('assign')

    >>> prospect1.assigned_operator.name
    'Administrator'
    >>> prospect1.state
    'assigned'
    >>> prospect2.assigned_operator.name
    'Administrator'
    >>> prospect2.state
    'assigned'


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


Verificar creación de seguimiento de prospecto::
    >>> ProspectTrace = Model.get('sale.prospect_trace')
    >>> prospect_trace, = ProspectTrace.find([('prospect', '=', prospect1)])

    >>> prospect_trace.prospect.name
    'guchito S.A.S'
    >>> prospect_trace.prospect_business_unit
    'brigade'
    >>> prospect_trace.prospect_city.name
    'Medellín'
    >>> prospect_trace.prospect_assigned_operator.name
    'Administrator'
    >>> prospect_trace.prospect_contacts
    [proteus.Model.get('prospect.contact_method')(1), proteus.Model.get('prospect.contact_method')(2), proteus.Model.get('prospect.contact_method')(3)]

Agregar un método de contacto desde el seguimiento de prospecto::
    >>> contact_method_ = prospect_trace.prospect_contacts.new(value='31231231212', name='Carlos', job='Supervisor')
    >>> contact_method_.prospect
    proteus.Model.get('sale.prospect')(1)


Crear llamadas a un seguimiento de prospecto::
    >>> make_call = Wizard('sale.prospect_trace.make_call', [prospect_trace])
    >>> make_call.form.description = 'First call to the prospect'
    >>> make_call.form.interest = '0'
    >>> make_call.form.schedule_call = 'no'
    >>> make_call.execute('make_call')
    >>> make_call.state
    'end'

    >>> make_call = Wizard('sale.prospect_trace.make_call', [prospect_trace])
    >>> make_call.form.description = 'Second call to the prospect'
    >>> make_call.form.interest = '1'
    >>> make_call.form.schedule_call = 'no'
    >>> make_call.execute('make_call')
    >>> make_call.state
    'end'

    >>> make_call = Wizard('sale.prospect_trace.make_call', [prospect_trace])
    >>> make_call.form.description = 'Third call to the prospect'
    >>> make_call.form.interest = '3'
    >>> make_call.form.schedule_call = 'yes'
    >>> make_call.execute('make_call')
    >>> make_call.form.datetime = datetime(2023, 8, 14, 15, 30, 30)
    >>> make_call.execute('schedule_call')


Verificar estado final del seguimiento del prospecto y sus llamadas::
    >>> prospect_trace.calls[0].call_result
    'missed_call'
    >>> prospect_trace.calls[0].call_type
    'first_call'
    >>> prospect_trace.calls[0].date == date.today()
    True
    >>> prospect_trace.calls[0].call_business_unit
    'brigade'
    >>> prospect_trace.calls[0].operator_who_called.name
    'Administrator'
    >>> prospect_trace.calls[1].call_result
    'answered_call'
    >>> prospect_trace.calls[1].call_type
    'followup_call'
    
    >>> prospect_trace.calls
    [proteus.Model.get('sale.call')(1), proteus.Model.get('sale.call')(2), proteus.Model.get('sale.call')(3)]
    >>> prospect_trace.pending_call.date
    datetime.datetime(2023, 8, 14, 15, 30, 30)
    >>> prospect_trace.current_interest
    '3'
    >>> prospect_trace.state 
    'with_pending_calls'

Programar una próxima llamada pendiente al seguimiento de prospecto::    
    >>> schedule = Wizard('sale.prospect_trace.schedule', [prospect_trace])
    >>> schedule.form.date_time = datetime(2023, 8, 14, 15, 30, 30)
    >>> schedule.execute('schedule')

    >>> prospect_trace.pending_call.date
    datetime.datetime(2023, 8, 14, 15, 30, 30)
    >>> prospect_trace.state
    'with_pending_calls'

Crear una llamada agendada previamente::
    >>> make_call = Wizard('sale.prospect_trace.make_call', [prospect_trace])
    >>> make_call.form.description = 'Fourth call to the prospect'
    >>> make_call.form.interest = '2'
    >>> make_call.execute('make_call')

    >>> prospect_trace.pending_call

    >>> prospect_trace.state
    'open'

Hacer llamada y programar tarea::
    >>> make_call = Wizard('sale.prospect_trace.make_call', [prospect_trace])
    >>> make_call.form.description = 'Prospect told me to send him an email'
    >>> make_call.form.interest = '3'
    >>> make_call.form.schedule_call = 'yes'
    >>> make_call.form.schedule_task = 'yes'
    >>> make_call.execute('make_call')
    >>> make_call.form.datetime = datetime(2023, 8, 14, 15, 30, 30)
    >>> make_call.execute('schedule_call')
    >>> make_call.form.task_description = 'I have to send a mail to prospect offering him this services...'
    >>> make_call.execute('schedule_task')

    >>> Task = Model.get('sale.pending_task')
    >>> task, = Task.find([('description', '=', 'I have to send a mail to prospect offering him this services...')])
    >>> task
    proteus.Model.get('sale.pending_task')(1)

    >>> task.state
    'pending'

    >>> task.click('close_task') 
    >>> task.state
    'done'

Hacer llamada y cerrar venta (Seguimiento de prospecto)::
    >>> make_call = Wizard('sale.prospect_trace.make_call', [prospect_trace])
    >>> make_call.form.description = 'Closed sale'
    >>> make_call.form.interest = '4'
    >>> make_call.execute('make_call')
    >>> prospect_trace.click('close_trace')

    >>> prospect_trace.state
    'closed'

Reabrir seguimiento a prospecto una vez cerrado::
    >>> prospect_trace.click('reopen_trace')
    >>> prospect_trace.state
    'open'

Reasignar prospectos por operador::
    >>> operator2 = User();
    >>> operator2.name = 'Operatus'
    >>> operator2.login = 'login'
    >>> operator2.save()

    >>> reassign_by_operator = Wizard('sale.prospect.reassign_by_operator', [])
    >>> reassign_by_operator.form.current_operator = user
    >>> reassign_by_operator.form.prospects
    [proteus.Model.get('sale.prospect')(1), proteus.Model.get('sale.prospect')(2)]
    >>> reassign_by_operator.form.new_operator = operator2
    >>> reassign_by_operator.execute('reassign_by_operator')

    >>> prospect1.reload()
    >>> prospect1.assigned_operator.name
    'Operatus'

    >>> prospect2.reload()
    >>> prospect2.assigned_operator.name
    'Operatus'

    >>> prospect_trace.reload()
    >>> prospect_trace.prospect_assigned_operator.name
    'Operatus'

    .. Las llamadas deben conservar el operador que las hizo
    >>> prospect_trace.calls[0].operator_who_called.name
    'Administrator'

Reasignar prospectos por prospecto::
    >>> reassign_by_prospect = Wizard('sale.prospect.reassign_by_prospect', [])
    >>> reassign_by_prospect.form.prospect = prospect1
    >>> reassign_by_prospect.form.new_operator = user
    >>> reassign_by_prospect.execute('reassign_by_prospect')
    

    >>> prospect1.reload()
    >>> prospect1.assigned_operator.name
    'Administrator'
    >>> prospect_trace.reload()
    >>> prospect_trace.prospect_assigned_operator.name
    'Administrator'
    >>> prospect_trace.calls[0].operator_who_called.name
    'Administrator'

Crear un usuario de rol administrador::
    >>> User = Model.get('res.user')
    >>> admin = User(name="Administrator", login="administrator", user_admin=True)
    >>> admin.save()
    >>> admin.user_admin == True
    True
    
Agregar un nuevo método de contacto desde prospecto
    >>> contact_method = prospect1.contact_methods.new(value='0000000000', name='Nuevo', job='Puesto increíble') 
    >>> prospect1.save()

    >>> prospect1.contact_methods[-1].value
    '0000000000'
    >>> prospect_trace.prospect_contacts[-1].value
    '0000000000'

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

* Reporte de seguimiento a prospecto (Análisis de prospecto):
    * Interés durante distintas etapas del seguimiento


* Reporte de Llamadas a realizar (Analisis de trabajo pendiente):
    * Llamadas pendientes
    * Seguimientos a prospectos abiertos

* Reporte de seguimientos sin asignar - asignados:
    * Seguimientos a prospectos pendientes por asignar a operador

* Reporte de prospectos potenciales
    * llamadas con un nivel de interés alto
    * Seguimiento de prospecto al que pertenecen las llamadas

