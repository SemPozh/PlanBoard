from django import template
from ..models import Plan

register = template.Library()


@register.inclusion_tag('planning/plans_by_template.html')
def plans_by_template(template_id):
    plans = Plan.objects.filter(template_id=template_id)
    if not plans:
        return {'plans': []}
    else:
        data_length = len(plans[0].data['plan_data'])
        return {'plans': plans}




