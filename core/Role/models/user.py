# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import PoolMeta


class User(metaclass=PoolMeta):
    "User"
    __name__ = 'res.user'

    user_admin = fields.Boolean('Is Admin')
    is_operator = fields.Boolean('Is Operator')

    @classmethod
    def __setup__(cls):
        super(User, cls).__setup__()
        cls._context_fields.insert(0, 'user_admin')
