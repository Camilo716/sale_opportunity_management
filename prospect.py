# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields
from trytond.pyson import Eval, If


class Prospect(ModelSQL, ModelView):
    'Prospecto'
    __name__ = 'sale.prospect'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)

    contact_methods = fields.One2Many(
        'prospect.contact_method',
        'prospect', 'Contact methods', required=True)

    department = fields.Many2One('sale.department', 'Department')
    city = fields.Many2One('sale.city', 'City',
                           domain=[If(Eval('department'),
                                    ('parent', '=', Eval('department')))])

    assigned_operator = fields.Many2One('res.user', "Assigned operator")

    state = fields.Selection([
        ('unassigned', 'Unsassigned'),
        ('assigned', 'Assigned')], "State", readonly=True)

    @classmethod
    def default_state(cls):
        return 'unassigned'

    @fields.depends('city', 'department')
    def on_change_city(self):
        if self.city:
            self.department = self.city.parent

    @fields.depends('assigned_operator', 'state')
    def on_change_assigned_operator(self):
        if self.assigned_operator:
            self.state = 'assigned'
        else:
            self.state = 'unassigned'


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
    job = fields.Char('job')

    prospect = fields.Many2One('sale.prospect', 'Prospect', required=True)

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
