# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
# from trytond.model import ModelSQL, ModelView, fields
from trytond.wizard import Wizard, StateView, Button  # , StateReport
from trytond.model import fields, ModelView


class PrintReportByOperatorStart(ModelView):
    'Vista inicial de reporte por operario'
    __name__ = 'sale.print_report_by_operator.start'

    start_date = fields.Date('Start date')
    end_date = fields.Date('End date')


class PrintReportByOperator(Wizard):
    'Generar reporte por operario'
    __name__ = 'sale.print_report_by_operator'

    start = StateView(
        'sale.print_report_by_operator.start',
        'sale_opportunity_management.print_report_by_operator_start_view_form',
        [Button("Cancel", "end", "tryton-cancel"),
         Button("Print Report", "print_report", "tryton-ok", default=True)])
