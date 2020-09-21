from django import template

register = template.Library()


@register.inclusion_tag('procurement_dashboard/buttons/purchase_order_button.html')
def purchase_order_button(model_wrapper):
    title = ['Edit purchase order form.']
    return dict(
        order_number=model_wrapper.object.order_number,
        href=model_wrapper.href,
        title=' '.join(title))
