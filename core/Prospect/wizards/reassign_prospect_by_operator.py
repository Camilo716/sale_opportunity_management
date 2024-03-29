# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.


from trytond.wizard import Wizard, StateView, Button, StateTransition
from trytond.model import ModelView, fields
from trytond.pool import Pool

from ....core.Prospect.wizards.assign_operator import GenericAssign


class ReassignProspectByOperatorStart(ModelView):
    'Inicio de reasignación de prospecto por operario'
    __name__ = 'sale.prospect.reassign_by_operator.start'

    current_operator = fields.Many2One(
        'res.user', "Current operator", required=True)
    new_operator = fields.Many2One(
        'res.user', "New operator", required=True)
    prospects = fields.One2Many(
        'sale.prospect', None, 'Prospects', readonly=True)

    @fields.depends('current_operator', 'prospects')
    def on_change_current_operator(self):
        pool = Pool()
        Prospect = pool.get('sale.prospect')

        self.prospects = []
        self.prospects = Prospect.search(
            [('state', '=', 'assigned'),
             ('assigned_operator', '=', self.current_operator)])


class ReassignProspectByOperator(Wizard):
    'Reasignar todos los prospectos de un operario, a otro operario'
    __name__ = 'sale.prospect.reassign_by_operator'

    start = StateView(
        'sale.prospect.reassign_by_operator.start',
        'sale_opportunity_management.reassign_by_operator_start_view_form',
        [Button("Cancel", 'end', 'tryton-cancel'),
         Button("Reassign", 'reassign_by_operator', 'tryton-ok', default=True)
         ])

    reassign_by_operator = StateTransition()

    def transition_reassign_by_operator(self):
        _prospects = self.start.prospects
        _operator = self.start.new_operator

        GenericAssign.assign_prospects_to_operator(_prospects, _operator)

        return 'end'
