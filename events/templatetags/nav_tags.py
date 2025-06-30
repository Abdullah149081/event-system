from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def nav_active(context, url):
    request = context["request"]
    return "text-[green] font-bold" if request.path.startswith(url) else ""
