Importaciones::

    >>> from proteus import Model, Wizard
    >>> from trytond.transaction import Transaction
    >>> from trytond.tests.tools import activate_modules, set_user

Activar módulos::

    >>> config = activate_modules('sale_opportunity_management')


Crear operario::
    >>> User = Model.get('res.user')
    >>> operator,  = User.find([('name', '=', 'Administrator')])
    >>> operator.is_operator = True
    >>> operator.save()
    >>> set_user(operator.id)

Crear prospecto::

    >>> Prospect = Model.get('sale.prospect')
    >>> prospect = Prospect()

    >>> prospect.name = 'Assignable To Me S.A.S'
    >>> contact_method = prospect.contact_methods.new(value='123123123', name='Ricardo', job='Infraestructura')  
    >>> prospect.business_unit = 'brigade'
    >>> prospect.save()


    [ Se inició seguimiento, asignado al operador que lo creó ]
    >>> ProspectTrace = Model.get('sale.prospect_trace')
    >>> prospect_trace, = ProspectTrace.find([('prospect', '=', prospect)])
    >>> assigned_operator_id = prospect_trace.prospect_assigned_operator.id
    >>> assert operator.id == assigned_operator_id

