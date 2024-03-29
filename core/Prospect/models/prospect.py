# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.model import ModelSQL, ModelView, fields, DeactivableMixin
from trytond.pyson import Eval, If
from trytond.transaction import Transaction
from trytond.pool import Pool
from ....core.Prospect.wizards.assign_operator import GenericAssign


class Prospect(ModelSQL, ModelView, DeactivableMixin):
    'Prospecto'
    __name__ = 'sale.prospect'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)

    business_unit = fields.Selection(
        [('brigade', 'Brigade'),
         ('optics', 'Optics'),
         ('equipment', 'Equipment')],
        'Business unit', required=True
    )

    contact_methods = fields.One2Many(
        'prospect.contact_method',
        'prospect', 'Contact methods', required=True)

    department = fields.Many2One('sale.department', 'Department')
    city = fields.Many2One('sale.city', 'City',
                           domain=[If(Eval('department'),
                                    ('parent', '=', Eval('department')))])

    assigned_operator = fields.Many2One(
        'res.user', "Assigned operator", readonly=True)

    state = fields.Selection([
        ('unassigned', 'Unsassigned'),
        ('assigned', 'Assigned')], "State", readonly=True)

    prospect_trace = fields.Many2One('sale.prospect_trace', 'Prospect trace')

    rating = fields.Selection(
        [(None, None),
         ('1', '1'),
         ('2', '2'),
         ('3', '3'),
         ('4', '4'),
         ('5', '5')], 'Rating (1-5)')
    comments = fields.Text('Comments')

    @classmethod
    def default_state(cls):
        return 'unassigned'

    @fields.depends('prospect_trace', 'contact_methods')
    def on_change_contact_methods(self):
        for contact in self.contact_methods:
            contact.prospect_trace = self.prospect_trace

    @fields.depends('city', 'department')
    def on_change_city(self):
        if self.city:
            self.department = self.city.parent

    @classmethod
    def create(cls, values):
        user_id = Transaction().user
        records = super().create(values)

        cls.try_assign_to_current_operator(records, user_id)
        return records

    @classmethod
    def try_assign_to_current_operator(cls, prospects, user_id):
        User = Pool().get('res.user')
        user, = User.search([('id', '=', user_id)])

        if user.is_operator:
            GenericAssign.assign_prospects_to_operator(prospects, user)
