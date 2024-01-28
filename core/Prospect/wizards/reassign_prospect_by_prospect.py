# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.


from trytond.wizard import Wizard, StateView, Button, StateTransition
from trytond.model import ModelView, fields
from trytond.pool import Pool


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
        pool = Pool()
        ProspectTrace = pool.get('sale.prospect_trace')

        self.start.prospect.assigned_operator = self.start.new_operator

        if self.start.prospect.prospect_trace:
            prospect_trace, = ProspectTrace.search(
                [('prospect', '=', self.start.prospect)])
            prospect_trace.prospect_assigned_operator =\
                self.start.new_operator
            prospect_trace.save()

        self.start.prospect.save()
        return 'end'
