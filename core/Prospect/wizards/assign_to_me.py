# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.wizard import Wizard, StateView, Button, StateTransition
from trytond.model import ModelView, fields


class AssignToMe(Wizard):
    'Asignar un prospecto al usuario actual'
    __name__ = 'sale.prospect.assign_to_me'

    start = StateView(
        model_name='sale.prospect.assign_to_me.start',
        view='sale_opportunity_management.assign_to_me_start_view_form',
        buttons=[
            Button("Cancel", 'end', 'tryton-cancel'),
            Button("Confirm", 'confirm', 'tryton-ok', default=True)
        ]
    )

    start = StateTransition()


class AssignToMeStart(ModelView):
    'Inicio de asignación de un prospecto al usuario actual'
    __name__ = 'sale.prospect.assign_to_me.start'

    assign_to_me = fields.Boolean("Assign to me?")
