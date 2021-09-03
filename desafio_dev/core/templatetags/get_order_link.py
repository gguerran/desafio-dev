from django import template

register = template.Library()


@register.simple_tag(name="get_order_link")
def get_order_link(field, full_path, path):
    url = path + '?'
    if 'number_page=' in full_path:
        url += full_path[full_path.find('number_page='):full_path.find('number_page=')+14] + '&'

    if f'={field}' in full_path:
        full_path = full_path.replace(f'={field}', f'=-{field}')
        return full_path

    if f'=-{field}' in full_path:
        full_path = full_path.replace(f'=-{field}', f'={field}')
        return full_path

    return f"{url}order_by={field}"
