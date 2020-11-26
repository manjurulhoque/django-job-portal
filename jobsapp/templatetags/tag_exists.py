from django import template

register = template.Library()


@register.simple_tag(name="tag_exists")
def tag_exists(id, tags):
    return True if tags is not None and len(tags) > 0 and str(id) in tags else False


@register.filter
def get_item(dictionary, key):
    return dict(dictionary).get(key)
