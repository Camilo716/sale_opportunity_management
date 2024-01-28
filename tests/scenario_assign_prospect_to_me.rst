.. Importaciones::

..     >>> from proteus import Model, Wizard
..     >>> from trytond.tests.tools import activate_modules

.. Activar módulos::

..     >>> config = activate_modules('sale_opportunity_management')


.. Crear operario::
..     >>> User = Model.get('res.user')
..     >>> operator = User(name="Operario", login="operario")

.. Crear prospecto::

..     >>> Prospect = Model.get('sale.prospect')
..     >>> prospect = Prospect()

..     >>> prospect.name = 'Assignable To Me S.A.S'
..     >>> contact_method = prospect.contact_methods.new(value='123123123', name='Ricardo', job='Infraestructura')  
..     >>> prospect.business_unit = 'brigade'
..     >>> prospect.save()

..     .. Opción 1:
..     .. [ Se abre una ventana preguntandole al usuario si quiere asignarse a sí mismo el prospecto recién creado ]
..     .. >>> assign_to_me_wizard = Wizard('sale.prospect.assign_to_me', [prospect])
..     .. >>> assign_to_me_wizard.form.assign_to_me = True
..     .. >>> assign_to_me_wizard.execute('assign_to_me')


..     ..Opcion2:
..     .. [Se evalua si el usuario actual es operador, de ser el caso se le asigna este prospecto]
..     [ Se inició seguimiento, asignado al operador que lo creó ]
..     >>> ProspectTrace = Model.get('sale.prospect_trace')
..     >>> prospect_trace, = ProspectTrace.find([('prospect', '=', prospect)])
..     >>> prospect_trace.prospect_assigned_operator.id
..     operator.id 

