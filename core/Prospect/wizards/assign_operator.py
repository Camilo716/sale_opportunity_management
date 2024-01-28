# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.


from trytond.wizard import Wizard, StateView, Button, StateTransition
from trytond.model import ModelView, fields
from trytond.pyson import Eval
from trytond.pool import Pool
from core.Prospect.models.prospect import Prospect

from core.ProspectTrace.models.prospect_trace import ProspectTrace


class AssignOperator(Wizard):
    'Asignar operador a prospecto'
    __name__ = 'sale.prospect.assign'

    start = StateView(
        'sale.prospect.assign.start',
        'sale_opportunity_management.assign_start_view_form', [
            Button("Cancel", 'end', 'tryton-cancel'),
            Button("Assign", 'assign', 'tryton-ok', default=True)])

    assign = StateTransition()

    def transition_assign(self):
        _prospects = self.start.prospects
        _operator = self.start.operator

        self._assign_operator(_prospects, _operator)

        return 'end'

    def _assign_operator(self, prospects, operator):

        for prospect in prospects:
            prospect.assigned_operator = operator
            prospect.state = 'assigned'

            prospect_trace = self._create_prospect_trace(prospect)

            prospect.prospect_trace = prospect_trace
            prospect.save()

    def _create_prospect_trace(self, prospect: Prospect) -> ProspectTrace:
        pool = Pool()
        ProspectTrace = pool.get('sale.prospect_trace')

        prospect_trace = ProspectTrace(
            prospect=prospect,
            prospect_city=prospect.city,
            prospect_business_unit=prospect.business_unit,
            prospect_assigned_operator=prospect.assigned_operator,
            prospect_contacts=prospect.contact_methods
        )

        prospect_trace.save()
        return prospect_trace


class AssignOperatorStart(ModelView):
    'Inicio de asignación de operador'
    __name__ = 'sale.prospect.assign.start'

    prospects_chunk = fields.Integer(
        'Prospects chunk', required=True,
        states={
            'readonly': ~Eval('business_unit', False)})

    operator = fields.Many2One('res.user', 'Operator', required=True)
    prospects = fields.One2Many(
        'sale.prospect', None, 'Prospects', readonly=True)

    business_unit = fields.Selection(
        [('brigade', 'Brigade'),
         ('optics', 'Optics'),
         ('equipment', 'Equipment')],
        'Business unit',
        states={
            'readonly': Eval('prospects_chunk', False)}
    )

    @classmethod
    def default_prospects_chunk(cls):
        return 0

    @fields.depends('prospects_chunk', 'prospects', 'business_unit')
    def on_change_prospects_chunk(self):
        pool = Pool()
        Prospect = pool.get('sale.prospect')

        if self.prospects_chunk >= 1:
            self.prospects = []
            self.prospects = Prospect.search(
                [('state', '=', 'unassigned'),
                 ('business_unit', '=', self.business_unit)],
                limit=self.prospects_chunk)
