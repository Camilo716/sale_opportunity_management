# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.wizard import Wizard, StateView, Button, StateTransition
from trytond.model import ModelView, fields
from trytond.pool import Pool
from trytond.pyson import Eval
from ....selections.call_types import CallTypes
from ....selections.interest import Interest
from datetime import datetime


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
