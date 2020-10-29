from django import template

register = template.Library()


@register.inclusion_tag('procurement_dashboard/buttons/purchase_order_button.html')
def purchase_order_button(model_wrapper):
    title = ['Edit purchase order form.']
    return dict(
        order_number=model_wrapper.object.order_number,
        href=model_wrapper.href,
        title=' '.join(title))


@register.inclusion_tag('procurement_dashboard/buttons/purchase_requisition_button.html')
def purchase_requisition_button(model_wrapper):
    title = ['Edit purchase requisition form.']
    return dict(
        prf_number=model_wrapper.object.prf_number,
        href=model_wrapper.href,
        title=' '.join(title))


@register.inclusion_tag('procurement_dashboard/buttons/request_approval_button.html')
def request_approval_button(model_wrapper):
    title = ['Edit request approval form.']
    return dict(
        rfa_number=model_wrapper.request_approval.rfa_number,
        document_id=model_wrapper.document_id,
        add_request_approval_href=model_wrapper.request_approval.href,
        request_approval_model_obj=model_wrapper.request_approval_model_obj,
        title=' '.join(title), )
