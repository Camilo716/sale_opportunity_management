# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields 

class ProspectTrace(ModelSQL, ModelView):
    'Seguimiento de un prospecto'
    
    __name__ = 'sale.prospect_trace'

    prospect = fields.Many2One('sale.prospect', 'Prospect')
    prospect_name = fields.Char('Name')
    prospect_contact = fields.Many2One('prospect.contact_method', 'Contact method')
    prospect_city = fields.Char('City') 

    calls = fields.One2Many('sale.call', 'prospect_trace', "Calls")

    @fields.depends('prospect')
    def on_change_prospect(self):
        if self.prospect:
            self.prospect_name = self.prospect.name
            # self.prospect_contact = self.prospect.contact_methods.index('contact_type 'mobile')
            self.prospect_city = self.prospect.city
