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
        document_id=model_wrapper.document_id,
        add_request_approval_href=model_wrapper.request_approval.href,
        request_approval_model_obj=model_wrapper.request_approval_model_obj,
        request_model_obj=model_wrapper.request_model_obj,
        title=' '.join(title), )


@register.inclusion_tag('procurement_dashboard/buttons/request_button.html')
def request_button(model_wrapper):
    title = ['Approval requests.']
    return dict(
        document_id=model_wrapper.document_id,
        add_request_href=model_wrapper.approval_request.href,
        request_approval_model_obj=model_wrapper.request_approval_model_obj,
        request_model_obj=model_wrapper.request_model_obj,
        request_approved=model_wrapper.request_approved,
        history_objects=model_wrapper.requests,
        title=' '.join(title), )


@register.inclusion_tag('procurement_dashboard/buttons/pending_request_button.html')
def pending_request_button(model_wrapper):
    title = ['Edit request approval form.']
    return dict(
        document_id=model_wrapper.document_id,
        add_request_approval_href=model_wrapper.request_approval.href,
        request_approval_model_obj=model_wrapper.request_approval_model_obj,
        request_model_obj=model_wrapper.request_model_obj,
        title=' '.join(title), )


@register.inclusion_tag('procurement_dashboard/buttons/vendor_justification_button.html')
def vendor_justification_button(model_wrapper):
    title = ['Edit vendor justification form.']
    return dict(
        prf_number=model_wrapper.prf_number,
        add_justification_href=model_wrapper.vendor_justification.href,
        vendor_justification_model_obj=model_wrapper.vendor_justification_model_obj,
        title=' '.join(title), )


@register.simple_tag
def justification_required(model_wrapper):
    cost = 0
    purchase_items = model_wrapper.object.purchaserequisitionitem_set.all()
    for item in purchase_items:
        cost += item.total_price_incl
    return True if cost > 5000.00 else False


@register.simple_tag
def purchase_order_model(model_wrapper):
    return model_wrapper.purchase_order.href


@register.simple_tag
def bhp_allocations(model_wrapper):
    names = []
    allocations = model_wrapper.object.allocation_set.all()
    for allocation in allocations:
        names.append(f'{allocation.bhp_allocation.name}({allocation.percentage}%)')
    return ', '.join(names)


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
