# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields
from .selections.interest import Interest


class ProspectTrace(ModelSQL, ModelView):
    'Seguimiento de un prospecto'

    __name__ = 'sale.prospect_trace'

    prospect = fields.Many2One('sale.prospect', 'Prospect')
    prospect_contact = fields.Many2One(
        'prospect.contact_method', 'Contact method')
    prospect_city = fields.Char('City')

    calls = fields.One2Many('sale.call', 'prospect_trace', "Calls")

    _interest_field_type = fields.Selection(
        Interest.get_interest_levels(), 'Current interest')
    current_interest = fields.Function(
        _interest_field_type, '_get_current_interest')

    @fields.depends('prospect')
    def on_change_prospect(self):
        if self.prospect:
            self.prospect_city = self.prospect.city

    def _get_current_interest(self, name):
        return self.calls[-1].interest
