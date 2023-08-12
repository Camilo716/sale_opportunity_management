# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool

from .selections.call_types import CallTypes
from .selections.interest import Interest
from .selections.prospect_trace_states import ProspectTraceStates


class ProspectTrace(ModelSQL, ModelView):
    'Seguimiento de un prospecto'
    __name__ = 'sale.prospect_trace'

    prospect = fields.Many2One('sale.prospect', 'Prospect', required=True)
    prospect_contact = fields.Many2One(
        'prospect.contact_method', 'Contact method')
    prospect_city = fields.Many2One('sale.city', 'City')

    calls = fields.One2Many('sale.call', 'prospect_trace', 'Calls')
    pending_calls = fields.One2Many(
        'sale.pending_call', 'prospect_trace', 'Pending calls')

    current_interest = fields.Selection(
        Interest.get_interest_levels(), 'Current interest')

    _states_selection = ProspectTraceStates.get_prospect_trace_states()
    state = fields.Selection(_states_selection, 'State')

    @fields.depends('calls', 'current_interest')
    def on_change_calls(self):
        if self.calls:
            last_call = self.calls[-1]
            self.current_interest = last_call.interest

            if len(self.calls) > 1:
                last_call.call_type = CallTypes.get_call_types()[1][0]
            else:
                last_call.call_type = CallTypes.get_call_types()[0][0]

    @fields.depends('pending_calls', 'state')
    def on_change_pending_calls(self):
        if self.pending_calls:
            with_pending_calls_state = self._states_selection[2][0]
            self.state = with_pending_calls_state

    @fields.depends('prospect')
    def on_change_prospect(self):
        if not self.prospect:
            return

        self.prospect_city = self.prospect.city
        mobile_contact = self._get_prospect_mobile_contact()

        if mobile_contact:
            self.prospect_contact = mobile_contact

        open_state = self._states_selection[1][0]
        self.state = open_state

    def get_rec_name(self, name):
        if self.prospect:
            return '[' + str(self.id) + '] ' + self.prospect.name

    def _get_current_interest(self, name):
        if self.calls:
            return self.calls[-1].interest

    def _get_prospect_mobile_contact(self):
        pool = Pool()
        ContactMethod = pool.get('prospect.contact_method')

        contact_mobile, = ContactMethod.search(
            [('prospect', '=', self.prospect.id),
            ('contact_type', '=', 'mobile')],
            limit=1)

        return contact_mobile
