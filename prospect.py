# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields
from trytond.pyson import Eval, If


class Prospect(ModelSQL, ModelView):
    'Prospecto'
    __name__ = 'sale.prospect'
    _rec_name = 'name'

    name = fields.Char('Name')

    contact_methods = fields.One2Many(
        'prospect.contact_method',
        'prospect', 'Contact methods', required=True)

    department = fields.Many2One('sale.department', 'Department')
    city = fields.Many2One('sale.city', 'City',
                           domain=[If(Eval('department'),
                                    ('parent', '=', Eval('department')))])

    @fields.depends('city', 'department')
    def on_change_city(self):
        if self.city:
            self.department = self.city.parent


class ContactMethod(ModelSQL, ModelView):
    'Mecanismo de contacto'
    __name__ = 'prospect.contact_method'

    _type = [
        ('phone', 'Phone'),
        ('mobile', 'Mobile'),
        ('mail', 'Mail')
    ]
    contact_type = fields.Selection(_type, 'Contact type')

    value = fields.Char('Value')
    name = fields.Char('Name')
    job = fields.Char('job')

    prospect = fields.Many2One('sale.prospect', 'Prospect')

    def get_rec_name(self, name):
        fields = [self.name, self.job, self.value]
        contact_rec_name = ''

        for field in fields:
            if field:
                contact_rec_name += ' [' + str(field) + '] '

        return contact_rec_name
