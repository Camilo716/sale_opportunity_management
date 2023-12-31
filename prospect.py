# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.wizard import Wizard, StateView, Button, StateTransition
from trytond.model import ModelSQL, ModelView, fields, DeactivableMixin
from trytond.pyson import Eval, If
from trytond.pool import Pool


class Prospect(ModelSQL, ModelView, DeactivableMixin):
    'Prospecto'
    __name__ = 'sale.prospect'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)

    business_unit = fields.Selection(
        [('brigade', 'Brigade'),
         ('optics', 'Optics'),
         ('equipment', 'Equipment')],
        'Business unit', required=True
    )

    contact_methods = fields.One2Many(
        'prospect.contact_method',
        'prospect', 'Contact methods', required=True)

    department = fields.Many2One('sale.department', 'Department')
    city = fields.Many2One('sale.city', 'City',
                           domain=[If(Eval('department'),
                                    ('parent', '=', Eval('department')))])

    assigned_operator = fields.Many2One(
        'res.user', "Assigned operator", readonly=True)

    state = fields.Selection([
        ('unassigned', 'Unsassigned'),
        ('assigned', 'Assigned')], "State", readonly=True)

    prospect_trace = fields.Many2One('sale.prospect_trace', 'Prospect trace')

    rating = fields.Selection(
        [(None, None),
         ('1', '1'),
         ('2', '2'),
         ('3', '3'),
         ('4', '4'),
         ('5', '5')], 'Rating (1-5)')
    comments = fields.Text('Comments')

    @classmethod
    def default_state(cls):
        return 'unassigned'

    @fields.depends('prospect_trace', 'contact_methods')
    def on_change_contact_methods(self):
        for contact in self.contact_methods:
            contact.prospect_trace = self.prospect_trace

    @fields.depends('city', 'department')
    def on_change_city(self):
        if self.city:
            self.department = self.city.parent


class ContactMethod(ModelSQL, ModelView):
    'Mecanismo de contacto'
    __name__ = 'prospect.contact_method'

    contact_type = fields.Selection([
        ('phone', 'Phone'),
        ('mobile', 'Mobile'),
        ('mail', 'Mail')
        ], 'Contact type', required=True)

    value = fields.Char('Value', required=True)
    name = fields.Char('Name')
    job = fields.Char('Job')

    prospect = fields.Many2One('sale.prospect', 'Prospect', required=True)
    prospect_trace = fields.Many2One(
        'sale.prospect_trace', 'Prospect Trace', required=False)

    @classmethod
    def default_contact_type(cls):
        return 'mobile'

    def get_rec_name(self, name):
        fields = [self.name, self.job, self.value]
        contact_rec_name = ''

        for field in fields:
            if field:
                contact_rec_name += ' [' + str(field) + '] '

        return contact_rec_name


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
        pool = Pool()
        ProspectTrace = pool.get('sale.prospect_trace')

        for prospect in self.start.prospects:
            prospect.assigned_operator = self.start.new_operator

            if prospect.prospect_trace:
                prospect_trace, = ProspectTrace.search(
                    [('prospect', '=', prospect)])
                prospect_trace.prospect_assigned_operator =\
                    self.start.new_operator
                prospect_trace.save()

            prospect.save()

        return 'end'


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
