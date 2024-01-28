# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.wizard import Wizard, StateView, Button, StateTransition
from trytond.model import ModelView, fields

from core.Prospect.wizards.assign_operator import GenericAssign


class ReassignProspectByProspectStart(ModelView):
    'Inicio de reasignación de un prospecto en específico'
    __name__ = 'sale.prospect.reassign_by_prospect.start'

    prospect = fields.Many2One(
        'sale.prospect', 'Prospect', required=True,
        domain=[('assigned_operator', '!=', None)])

    new_operator = fields.Many2One('res.user', "New operator", required=True)


class ReasignProspectByProspect(Wizard):
    'Reasignar un prospecto en específico a un nuevo operario'
    __name__ = 'sale.prospect.reassign_by_prospect'

    start = StateView(
        'sale.prospect.reassign_by_prospect.start',
        'sale_opportunity_management.reassign_by_prospect_start_view_form',
        [Button("Cancel", 'end', 'tryton-cancel'),
         Button("Reassign", 'reassign_by_prospect', 'tryton-ok', default=True)
         ])

    reassign_by_prospect = StateTransition()

    def transition_reassign_by_prospect(self):
        _prospect = self.start.prospect
        _operator = self.start.new_operator

        GenericAssign.assign_prospects_to_operator([_prospect], _operator)

        return 'end'
