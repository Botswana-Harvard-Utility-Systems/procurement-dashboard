import math
from django.views.generic.base import ContextMixin


class PurchaseOrderCalcMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        model_obj = self.model_obj(**kwargs)
        model_obj_set = self.model_obj_set(model_obj)
        overall_sum_excl = self.overall_total(model_obj_set, 'total_price_excl')
        overall_sum_incl = self.overall_total(model_obj_set, 'total_price_incl')
        vat = self.vat(overall_sum_excl)
        overall_disc = self.overall_discount(model_obj_set)
        overall_disc_sum = self.overall_incl_disc(overall_sum_incl, overall_disc)
        context = super().get_context_data(**kwargs)
        context.update(
            overall_sum_excl=overall_sum_excl,
            overall_sum_incl=overall_sum_incl,
            vat=vat,
            overall_disc=overall_disc,
            overall_disc_sum=overall_disc_sum)

        return context

    def overall_total(self, model_obj_set, field_name):
        unit_total = [getattr(unit, field_name) for unit in model_obj_set]
        return math.fsum(unit_total)

    def vat(self, overall_sum_excl):
        return (overall_sum_excl * 0.12)

    def check_sum_incl(self, overall_sum_excl, overall_sum_incl, vat):
        return True if (overall_sum_excl + vat) == overall_sum_incl else False

    def overall_discount(self, model_obj_set):
        unit_disc = [(obj.unit_price * obj.discount) for obj in model_obj_set]
        overal_disc = math.fsum(unit_disc)
        return overal_disc

    def overall_incl_disc(self, overall_sum_incl, discount):
        return overall_sum_incl - discount
