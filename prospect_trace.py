# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields

from .selections.call_types import CallTypes
from .selections.interest import Interest
from .selections.prospect_trace_states import ProspectTraceStates


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

    current_interest = fields.Selection(
        Interest.get_interest_levels(), 'Current interest')

    _state_type_field = fields.Selection(
        ProspectTraceStates.get_prospect_trace_states(), 'State')
    state = fields.Function(_state_type_field, '_get_state')

    @fields.depends('calls', 'current_interest')
    def on_change_calls(self):
        if self.calls:
            last_call = self.calls[-1]
            self.current_interest = last_call.interest

            if len(self.calls) > 1:
                last_call.call_type = CallTypes.get_call_types()[1][0]
            else:
                last_call.call_type = CallTypes.get_call_types()[0][0]

    @fields.depends('prospect')
    def on_change_prospect(self):
        if self.prospect:
            self.prospect_city = self.prospect.city

    def get_rec_name(self, name):
        if self.prospect:
            return '[' + str(self.id) + '] ' + self.prospect.name

    def _get_state(self, name):
        has_pending_calls = len(self.pending_calls) > 0

        if has_pending_calls:
            return ProspectTraceStates.get_prospect_trace_states()[2][0]
        else:
            return ProspectTraceStates.get_prospect_trace_states()[1][0]

    def _get_current_interest(self, name):
        if self.calls:
            return self.calls[-1].interest
