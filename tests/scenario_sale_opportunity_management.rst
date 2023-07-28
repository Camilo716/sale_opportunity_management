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
    >>> prospect.city = 'Bogotá'
    >>> prospect.save()


-----------------------------------------------------------------------------------------
Como operador quiero poder crear un seguimiento de prospecto para luego hacer una llamada
-----------------------------------------------------------------------------------------

Crear seguimiento de prospecto::
    >>> ProspectTracker = Model.get('sale.prospect_tracker')
    >>> prospect_tracker = ProspectTracker()

    >>> prospect_tracker.prospect = prospect
    >>> prospect_tracker.save()

    >>> prospect_tracker.prospect_name
    'guchito S.A.S'
    >>> prospect_tracker.prospect_tel 
    3123423422
    >>> prospect_tracker.prospect_city

----------------------------------------------------------------------------
Como operador quiero poder registrar una llamada para luego generar reportes
----------------------------------------------------------------------------

Crear llamada a un seguimiento de prospecto::
    >>> Call = Model.get('sale.call')
    >>> call = Call()

    >>> call.description = 'Descripción u observaciones de la llamada'
    >>> call.prospect_tracker = prospect_tracker
    >>> call.save()

    >>> call.prospect_tracker.prospect_name
    'guchito S.A.S'
    >>> call.prospect_tracker.prospect_tel 
    3123423422
    >>> call.date == date.today()
    True

Crear otra llamada al mismo seguimiento de prospecto::
    >>> Call = Model.get('sale.call')
    >>> call = Call()

    >>> call.description = 'Segunda llamada al mismo seguimiento'
    >>> call.prospect_tracker = prospect_tracker
    >>> call.save()

    >>> call.prospect_tracker.prospect_name
    'guchito S.A.S'
    >>> call.prospect_tracker.prospect_tel 
    3123423422
    >>> call.date == date.today()
    True
    >>> len(prospect_tracker.calls) == 2
    True