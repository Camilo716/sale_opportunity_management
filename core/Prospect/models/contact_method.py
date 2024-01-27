# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.model import ModelSQL, ModelView, fields


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
