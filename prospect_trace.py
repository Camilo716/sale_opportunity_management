# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields 

class ProspectTrace(ModelSQL, ModelView):
    'Seguimiento de un prospecto'
    
    __name__ = 'sale.prospect_trace'

    prospect = fields.Many2One('sale.prospect', 'Prospect')
    prospect_name = fields.Char('Name')
    prospect_tel = fields.Integer('Tel')

    calls = fields.One2Many('sale.call', 'prospect_trace', "Calls")

    @fields.depends('prospect')
    def on_change_prospect(self):
        if self.prospect:
            self.prospect_name = self.prospect.name
            self.prospect_tel = self.prospect.tel
