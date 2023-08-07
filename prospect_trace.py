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
    prospect_city = fields.Many2One('sale.city', 'City')

    calls = fields.One2Many('sale.call', 'prospect_trace', 'Calls')
    pending_calls = fields.One2Many(
        'sale.pending_call', 'prospect_trace', 'Pending calls')

    _interest_field_type = fields.Selection(
        Interest.get_interest_levels(), 'Current interest')
    current_interest = fields.Function(
        _interest_field_type, '_get_current_interest')

    def get_rec_name(self, name):
        if self.prospect:
            return '[' + self.id + '] ' + self.prospect.name

    @fields.depends('prospect')
    def on_change_prospect(self):
        if self.prospect:
            self.prospect_city = self.prospect.city

    def _get_current_interest(self, name):
        if self.calls:
            return self.calls[-1].interest
