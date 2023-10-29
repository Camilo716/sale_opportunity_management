# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.wizard import Wizard, StateView, Button, StateTransition
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool
from trytond.pyson import Eval
from .selections.call_types import CallTypes
from .selections.interest import Interest
from datetime import datetime


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
    tasks = fields.One2Many(
        'sale.pending_task', 'prospect_trace',
        'Pending Tasks', states=_states)

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
            contact.update_collaborators(changed_from='prospect_trace')

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


class ScheduleCallStart(ModelView):
    'Inicio agendar llamada a seguimiento de prospecto'
    __name__ = 'sale.prospect_trace.schedule.start'

    currency_date = fields.DateTime('Currency Date', readonly=True)
    date_time = fields.DateTime('Date time', domain=[
        ('date_time', '>=', Eval('currency_date'))])

    @classmethod
    def default_currency_date(cls):
        date = datetime.now()

        return date


class ScheduleCall(Wizard):
    'Agendar llamada a seguimiento de prospecto'
    __name__ = 'sale.prospect_trace.schedule'

    start = StateView(
        'sale.prospect_trace.schedule.start',
        'sale_opportunity_management.schedule_start_view_form', [
            Button("Cancel", 'end', 'tryton-cancel'),
            Button("Schedule", 'schedule', 'tryton-ok', default=True)])

    schedule = StateTransition()

    def transition_schedule(self):
        MakeCall.create_schedule_call(self.start.date_time, self.record)
        return 'end'


class MakeCallStart(ModelView):
    'Inicio de creación de llamada a seguimiento de prospecto'
    __name__ = 'sale.prospect_trace.make_call.start'

    description = fields.Text('Description')
    interest = fields.Selection(
        Interest.get_interest_levels(), 'Interest', required=True)
    schedule_call = fields.Selection(
        [('yes', 'Yes'),
         ('no', 'No')], 'Schedule call?', required=True)

    schedule_task = fields.Selection(
        [('yes', 'Yes'),
         ('no', 'No')], 'Schedule task?', required=True)


class MakeCallAsk(ModelView):
    'Posible agendación de llamada luego de hacer llamada actual'
    __name__ = 'sale.prospect_trace.make_call.ask'

    currency_date = fields.DateTime('Currency Date', readonly=True)
    datetime = fields.DateTime('Date time', domain=[
        ('datetime', '>=', Eval('currency_date'))])

    @classmethod
    def default_currency_date(cls):
        date = datetime.now()

        return date


class MakeCallAskTask(ModelView):
    'Posible agendación de tarea luego de hacer llamada actual'
    __name__ = 'sale.prospect_trace.make_call.ask_task'

    task_description = fields.Text('Task description')


class MakeCall(Wizard):
    'Crear llamada a un seguimiento de prospecto'
    __name__ = 'sale.prospect_trace.make_call'

    start = StateView(
        'sale.prospect_trace.make_call.start',
        'sale_opportunity_management.make_call_start_view_form', [
            Button("Cancel", 'end', 'tryton-cancel'),
            Button("Make call", 'make_call', 'tryton-ok', default=True)])
    make_call = StateTransition()

    ask = StateView(
        'sale.prospect_trace.make_call.ask',
        'sale_opportunity_management.make_call_ask_view_form', [
            Button("Cancel", 'end', 'tryton-cancel'),
            Button(
                "Schedule call", 'schedule_call', 'tryton-ok', default=True)])
    schedule_call = StateTransition()

    ask_task = StateView(
        'sale.prospect_trace.make_call.ask_task',
        'sale_opportunity_management.make_call_ask_task_view_form', [
            Button("Cancel", 'end', 'tryton-cancel'),
            Button("Schedule task", 'schedule_task', 'tryton-ok', default=True)
        ]
    )
    schedule_task = StateTransition()

    def transition_make_call(self):
        prospect_trace = self.record

        pool = Pool()
        Call = pool.get('sale.call')
        call = Call()
        call.description = self.start.description
        call.interest = self.start.interest
        call.prospect_trace = self.record
        call.call_business_unit = self.record.prospect_business_unit
        call.operator_who_called = self.record.prospect_assigned_operator

        if call.interest == '0':
            call.call_result = 'missed_call'
        else:
            call.call_result = 'answered_call'
        already_exist_a_call = len(prospect_trace.calls) >= 1
        if already_exist_a_call:
            followup_call_type = CallTypes.get_call_types()[1][0]
            call.call_type = followup_call_type
        else:
            first_call_type = CallTypes.get_call_types()[0][0]
            call.call_type = first_call_type
        call.save()

        prospect_trace.current_interest = call.interest
        if prospect_trace.pending_call:
            prospect_trace.pending_call = None
            prospect_trace.state = 'open'
        prospect_trace.calls += (call,)
        prospect_trace.save()

        if self.start.schedule_call == 'yes':
            return 'ask'
        if self.start.schedule_task == 'yes':
            return 'ask_task'
        return 'end'

    def transition_schedule_task(self):
        self.create_schedule_task(self.ask_task.task_description, self.record)
        return 'end'

    def transition_schedule_call(self):
        self.create_schedule_call(self.ask.datetime, self.record)

        if (self.start.schedule_call and self.start.schedule_task) == 'yes':
            return 'ask_task'
        return 'end'

    @classmethod
    def create_schedule_task(cls, description, prospect_trace):
        pool = Pool()
        Task = pool.get('sale.pending_task')
        task = Task()
        task.description = description
        task.prospect_trace = prospect_trace
        task.contacts = prospect_trace.prospect_contacts
        task.save()

    @classmethod
    def create_schedule_call(cls, datetime, prospect_trace):
        pool = Pool()
        PendingCall = pool.get('sale.pending_call')
        pending_call = PendingCall()
        pending_call.date = datetime
        pending_call.save()

        prospect_trace.pending_call = pending_call
        prospect_trace.state = 'with_pending_calls'
        prospect_trace.save()
