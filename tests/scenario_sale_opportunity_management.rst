====================================
Sale Opportunity Management Scenario
====================================

Imports::

    >>> from proteus import Model, Wizard
    >>> from trytond.tests.tools import activate_modules
    >>> from datetime import date

Activate modules::

    >>> config = activate_modules('sale_opportunity_management')

---------------------------------------------------------------------------------------------
Como administrador quiero registrar un prospecto para lugo poder hacerle un seguimiento
---------------------------------------------------------------------------------------------

Crear mecanismos de contacto::


Crear prospecto::
    >>> Prospect = Model.get('sale.prospect')
    >>> prospect = Prospect()

    >>> prospect.name = 'guchito S.A.S'
    >>> prospect.city = 'Bogotá'
    >>> phone = prospect.contact_methods.new()
    >>> phone.contact_type = 'mobile'
    >>> phone.value = '3132923938'
    >>> prospect.save()



-----------------------------------------------------------------------------------------
Como operador quiero poder crear un seguimiento de prospecto para luego hacer una llamada
-----------------------------------------------------------------------------------------

Crear seguimiento de prospecto::
    >>> ProspectTrace = Model.get('sale.prospect_trace')
    >>> prospect_trace = ProspectTrace()

    >>> prospect_trace.prospect = prospect
    >>> prospect_trace.save()

    >>> prospect_trace.prospect_name
    'guchito S.A.S'
    >>> prospect_trace.prospect_city
    'Bogotá'

----------------------------------------------------------------------------
Como operador quiero registrar una llamada para luego generar reportes
----------------------------------------------------------------------------

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