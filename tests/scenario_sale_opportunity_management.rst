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
Como administrador quiero poder registrar un prospecto para lugo poder hacerle un seguimiento
---------------------------------------------------------------------------------------------

Crear prospecto::
    >>> Prospect = Model.get('sale.prospect')
    >>> prospect = Prospect()
    >>> prospect.name = 'guchito S.A.S'
    >>> prospect.tel = 3123423422
    >>> prospect.save()


-----------------------------------------------------------------------------------------
Como operador quiero poder crear un seguimiento de prospecto para luego hacer una llamada
-----------------------------------------------------------------------------------------

Crear seguimiento de prospecto::
    >>> ProspectTrace = Model.get('sale.prospect_trace')
    >>> prospect_trace = ProspectTrace()
    >>> prospect_trace.prospect = prospect

    >>> prospect_trace.prospect_name
    'guchito S.A.S'
    >>> prospect_trace.prospect_tel 
    3123423422

----------------------------------------------------------------------------
Como operador quiero poder registrar una llamada para luego generar reportes
----------------------------------------------------------------------------

Crear llamada a un seguimiento de prospecto::
    >>> Call = Model.get('sale.call')
    >>> call = Call()

    >>> call.date == date.today()
    True
