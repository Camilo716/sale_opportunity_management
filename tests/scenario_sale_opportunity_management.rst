====================================
Sale Opportunity Management Scenario
====================================

Imports::

    >>> from proteus import Model, Wizard
    >>> from trytond.tests.tools import activate_modules

Activate modules::

    >>> config = activate_modules('sale_opportunity_management')

---------------------------------------------------------------------------------------------
Como administrador quiero poder registrar un prospecto para lugo poder hacerle un seguimiento
---------------------------------------------------------------------------------------------

Crear prospecto::
    >>> Prospect = Model.get('call.prospect')
    >>> prospect = Prospect()
    >>> prospect.name = 'guchito S.A.S'
    >>> prospect.save()