# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields, DeactivableMixin
from trytond.pool import Pool

from .selections.call_types import CallTypes
from .selections.interest import Interest


class ProspectTrace(DeactivableMixin, ModelSQL, ModelView):
    'Seguimiento de un prospecto'
    __name__ = 'sale.prospect_trace'

    prospect = fields.Many2One('sale.prospect', 'Prospect', required=True)
    prospect_contact = fields.Many2One(
        'prospect.contact_method', 'Contact method')
    prospect_city = fields.Many2One('sale.city', 'City',
                                    states={'readonly': True})

    calls = fields.One2Many('sale.call', 'prospect_trace', 'Calls')
    pending_call = fields.Many2One('sale.pending_call', 'Pending call')

    current_interest = fields.Selection(
        Interest.get_interest_levels(), 'Current interest')

    state = fields.Selection([
            ('unassigned', 'Unassigned'),
            ('open', 'Open'),
            ('with_pending_calls', 'With pending calls'),
            ('closed', 'Closed')
            ], 'State')

    @classmethod
    def default_state(cls):
        return 'open'

    @fields.depends('calls', 'pending_call', 'current_interest', 'state')
    def on_change_calls(self):
        if not self.calls:
            return

        last_call = self.calls[-1]
        self.current_interest = last_call.interest

        already_exist_a_call = len(self.calls) > 1
        if already_exist_a_call:
            followup_call_type = CallTypes.get_call_types()[1][0]
            last_call.call_type = followup_call_type
        else:
            first_call_type = CallTypes.get_call_types()[0][0]
            last_call.call_type = first_call_type

        if self.pending_call:
            self.pending_call = None
            self.state = 'open'

    @fields.depends('pending_call', 'state')
    def on_change_pending_call(self):
        if self.pending_call:
            self.state = 'with_pending_calls'

    @fields.depends('prospect', 'prospect_city', 'prospect_contact')
    def on_change_prospect(self):
        if not self.prospect:
            self.prospect_city = None
            self.prospect_contact = None
            return

        self.prospect_city = self.prospect.city
        mobile_contact = self._get_prospect_mobile_contact()

        if mobile_contact:
            self.prospect_contact = mobile_contact

    def get_rec_name(self, name):
        if self.prospect:
            return '[' + str(self.id) + '] ' + self.prospect.name

    def _get_current_interest(self, name):
        if self.calls:
            return self.calls[-1].interest

    def _get_prospect_mobile_contact(self):
        pool = Pool()
        ContactMethod = pool.get('prospect.contact_method')

        contact_mobile = ContactMethod.search(
            [('prospect', '=', self.prospect.id),
            ('contact_type', '=', 'mobile')],
            limit=1)

        if contact_mobile:
            return contact_mobile[0]
