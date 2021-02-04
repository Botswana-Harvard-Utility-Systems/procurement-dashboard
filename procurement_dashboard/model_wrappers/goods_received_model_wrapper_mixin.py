from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from .goods_received_note_model_wrapper import GoodsReceivedNoteModelWrapper


class GoodsReceivedNoteModelWrapperMixin:

    goods_received_model_wrapper_cls = GoodsReceivedNoteModelWrapper

    @property
    def goods_received_model_obj(self):
        """Returns a goods received model instance or None.
        """
        try:
            return self.goods_received_cls.objects.get(
                **self.goods_received_options)
        except ObjectDoesNotExist:
            return None

    @property
    def goods_received(self):
        """Returns a wrapped saved or unsaved goods received note.
        """
        model_obj = self.goods_received_model_obj or self.goods_received_cls(
            **self.create_goods_received_options)
        return self.goods_received_model_wrapper_cls(model_obj=model_obj)

    @property
    def goods_received_cls(self):
        return django_apps.get_model('procurement.goodsreceivednote')

    @property
    def create_goods_received_options(self):
        """Returns a dictionary of options to create a new
        unpersisted goods received model instance.
        """
        options = dict(
            order_number=self.order_number,
            vendor=self.vendor, )
        return options

    @property
    def goods_received_options(self):
        """Returns a dictionary of options to get an existing
        goods received instance.
        """
        options = dict(
            order_number=self.order_number, )
        return options
