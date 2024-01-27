# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.


from trytond.wizard import Wizard, StateView, Button, StateTransition
from trytond.model import ModelView, fields
from trytond.pyson import Eval
from trytond.pool import Pool


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
        pool = Pool()
        ProspectTrace = pool.get('sale.prospect_trace')

        for prospect in self.start.prospects:
            prospect.assigned_operator = self.start.operator
            prospect.state = 'assigned'
            prospect.save()

            prospect_trace = ProspectTrace(
                prospect=prospect,
                prospect_city=prospect.city,
                prospect_business_unit=prospect.business_unit,
                prospect_assigned_operator=prospect.assigned_operator,
                prospect_contacts=prospect.contact_methods
            )
            prospect_trace.save()

            prospect.prospect_trace = prospect_trace
            prospect.save()

        return 'end'
