# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.model import ModelSQL, ModelView, fields
from trytond.pyson import Eval


class PendingTask(ModelSQL, ModelView):
    'Tarea a realizar a un seguimiento de prospecto'
    __name__ = "sale.pending_task"

    description = fields.Text(
        'Description', required=True,
        states={
            'readonly': Eval('state') == 'done'
        })

    state = fields.Selection(
        [('pending', 'Pending'),
        ('done', 'Done')],
        'State')

    prospect_trace = fields.Many2One(
        'sale.prospect_trace', 'Prospect trace',
        required=True, readonly=True)

    @classmethod
    def __setup__(cls):
        super(PendingTask, cls).__setup__()
        cls._buttons.update({
            'close_task': {
                'invisible': Eval('state') == 'done'
                }
            })

    @classmethod
    @ModelView.button
    def close_task(cls, tasks):
        for task in tasks:
            task.state = 'done'
            task.save()

    @classmethod
    def default_state(cls):
        return 'pending'
