from django import template
from ..models import Plan, Field, Template
from django.utils.safestring import mark_safe
from datetime import datetime
register = template.Library()


@register.inclusion_tag('planning/plans_by_template.html')
def plans_by_template(templates):
    if templates:
        plans = Plan.objects.filter(template_id=templates[0].id)
        if not plans:
            return {'plans': []}
        else:
            # data_length = len(plans[0].data['plan_data'])
            return {'plans': plans}


@register.inclusion_tag('planning/input_generation.html')
def generate_input(field_id, template_id):
    template_data = Template.objects.get(id=template_id)
    fields = template_data.fields['data']
    fields_html = []
    for field in fields:
        elem_id = field['elem_id']
        field_object = Field.objects.get(id=field['field_id'])
        if str(field['field_id']) in ['1', '3', '7', '8', '9']:
            if str(field['field_id']) == '7':
                try:
                    field['attrs']['default_value'] = datetime.strptime(field['attrs']['default_value'],
                                                                        '%d.%m.%Y').strftime('%Y-%m-%d')
                except:
                    pass

            field_html = f'<div class="input_wrapper" field_id={field["field_id"]}>' \
                            f'<label class="input_label" for="name{elem_id}">{field["attrs"]["label"]}</label>' \
                            f'<input type="{field_object.input_name.title}" class="{field_object.input_name.css_class} field_elem" field_id={field["field_id"]} name="name{elem_id}" style="height:{field["attrs"]["height"]}px" maxlength="{field["attrs"]["maxlength"]}" value="{field["attrs"]["default_value"]}">' \
                            f'<a href="#popup{elem_id}" class="popup-link"><i class="fas fa-sliders-h input_settings" field_id={field_id}></i></a>' \
                            f'<i class="fas fa-trash delete_input" elem_id={elem_id} field_id={field["field_id"]}></i>'\
                         f'</div>'
        elif str(field['field_id']) == '2':
            field_html = f'<div class="textarea_wrapper" field_id={field["field_id"]}>' \
                         f'<label class="input_label" for="name{elem_id}">{field["attrs"]["label"]}</label>' \
                         f'<textarea class="{field_object.input_name.css_class} field_elem" name="name{elem_id}" field_id={field["field_id"]} style="height:{field["attrs"]["height"]}px" maxlength="{field["attrs"]["maxlength"]}">{field["attrs"]["default_value"]}</textarea>' \
                         f'<a href="#popup{elem_id}" class="popup-link"><i class="fas fa-sliders-h input_settings" field_id={field_id}></i></a>' \
                         f'<i class="fas fa-trash delete_input" elem_id={elem_id} field_id={field["field_id"]}></i>'\
                         f'</div>'
        elif str(field['field_id']) in ['4', '5']:

            all_options = ''
            for option in field['attrs']['options']:
                if option == field['attrs']['default_value']:
                    is_checked = 'checked'
                else:
                    is_checked = ''
                all_options = all_options + f'<label class="{field_object.input_name.css_class}_label">' \
                                            f'<input type={field_object.input_name.title} class="{field_object.input_name.css_class}" name="name{elem_id}" value="{option}" {is_checked}>' \
                                            f'<span class="{field_object.input_name.css_class}_fake"></span>' \
                                            f'<span class="text">{option}</span>' \
                                            f'</label>'
            field_html = f'<div field_id={field["field_id"]}>' \
                         f'<label class="input_label_for_button" for="name{elem_id}">{field["attrs"]["label"]}</label>' \
                         f'<div class="button_input field_elem" field_id={field["field_id"]}>' \
                         f'<div class="button_wrap" elem_id={elem_id}>' \
                         f'{all_options}' \
                         f'</div>' \
                         f'<a href="#popup{elem_id}" class="popup-link"><i class="fas fa-sliders-h input_settings" field_id={field_id}></i></a>' \
                         f'<i class="fas fa-trash delete_input" elem_id={elem_id} field_id={field["field_id"]}></i>'\
                         f'</div>' \
                         f'</div>'
        elif str(field['field_id']) == '6':
            all_options = ''
            for option in field['attrs']['options']:
                if option == field['attrs']['default_value']:
                    is_selected = 'selected'
                else:
                    is_selected = ''
                all_options = all_options + f'<option value="{option}" class="select_option" {is_selected}>{option}</option>'
            field_html = f'<div class="select_wrapper" field_id={field["field_id"]} style="height:{field["attrs"]["height"]}px">' \
                         f'<label class="input_label" for="name{elem_id}">{field["attrs"]["label"]}</label>' \
                         f'<div class="select_wrap">' \
                         f'<select class="{field_object.input_name.css_class} field_elem" field_id={field["field_id"]}>' \
                         f'{all_options}' \
                         f'</select>' \
                         f'</div>' \
                         f'<a href="#popup{elem_id}" class="popup-link"><i class="fas fa-sliders-h input_settings" field_id={field_id}></i></a>' \
                         f'<i class="fas fa-trash delete_input" elem_id={elem_id} field_id={field["field_id"]}></i>'\
                         f'</div>'
        else:
            field_html = ''

        fields_html.append(mark_safe(field_html))
    return {'fields_html': fields_html}


@register.inclusion_tag('planning/popup_generation.html')
def generate_popup(template_id):
    template_data = Template.objects.get(id=template_id).fields

    return {
        'data': template_data['data']
    }
