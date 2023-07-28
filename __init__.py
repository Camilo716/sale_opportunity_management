from trytond.pool import Pool
from . import prospect

__all__ = ['register']


def register():
    Pool.register(
        prospect.Prospect,
        module='sale_opportunity_management', type_='model')
    Pool.register(
        module='sale_opportunity_management', type_='wizard')
    Pool.register(
        module='sale_opportunity_management', type_='report')
