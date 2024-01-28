# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.model import ModelSQL, ModelView, fields
from trytond.pyson import Eval
from selections.interest import Interest


class ProspectTrace(ModelSQL, ModelView):
    'Seguimiento de un prospecto'
    __name__ = 'sale.prospect_trace'

    _states = {'readonly': True}

    prospect = fields.Many2One(
        'sale.prospect', 'Prospect', required=True, states=_states)
    prospect_business_unit = fields.Selection(
        [('brigade', 'Brigade'),
         ('optics', 'Optics'),
         ('equipment', 'Equipment')],
        'Business unit', states=_states
    )
    prospect_contacts = fields.One2Many(
        'prospect.contact_method', 'prospect_trace',
        'Prospect contacts', required=True)
    prospect_city = fields.Many2One('sale.city', 'City',
                                    states=_states)

    prospect_assigned_operator = fields.Many2One(
        'res.user', "Assigned operator", states=_states)

    calls = fields.One2Many(
        'sale.call', 'prospect_trace', 'Calls', states=_states)
    pending_call = fields.Many2One(
        'sale.pending_call', 'Pending call', states=_states)

    current_interest = fields.Selection(
        Interest.get_interest_levels(), 'Current interest',
        states=_states)

    state = fields.Selection([
            ('unassigned', 'Unassigned'),
            ('open', 'Open'),
            ('with_pending_calls', 'With pending calls'),
            ('closed', 'Closed')
            ], 'State',
            states=_states)

    @fields.depends('prospect_contacts', 'prospect')
    def on_change_prospect_contacts(self):
        for contact in self.prospect_contacts:
            contact.prospect = self.prospect

    @classmethod
    def __setup__(cls):
        super(ProspectTrace, cls).__setup__()
        cls._buttons.update({
            'wizard_schedule': {
                'invisible': Eval('state') == 'with_pending_calls',
            },
            'wizard_make_call': {},
            'close_trace': {
                'invisible': Eval('state') == 'closed',
                'depends': ['state']
            },
            'reopen_trace': {
                'invisible': (Eval('state') == 'open')
                | (Eval('state') == 'with_pending_calls'),

                'depends': ['state']
            }
        })

    @classmethod
    def default_state(cls):
        return 'open'

    @classmethod
    @ModelView.button_action(
        'sale_opportunity_management.schedule_call_wizard')
    def wizard_schedule(cls, prospect_traces):
        pass

    @classmethod
    @ModelView.button_action(
        'sale_opportunity_management.make_call_wizard')
    def wizard_make_call(cls, prospect_traces):
        pass

    @classmethod
    @ModelView.button
    def close_trace(cls, prospect_traces):
        for prospect_trace in prospect_traces:
            prospect_trace.state = 'closed'
            prospect_trace.save()

    @classmethod
    @ModelView.button
    def reopen_trace(cls, prospect_traces):
        for prospect_trace in prospect_traces:
            prospect_trace.state = 'open'
            prospect_trace.save()

    def get_rec_name(self, name):
        if self.prospect:
            return '[' + str(self.id) + '] ' + self.prospect.name
