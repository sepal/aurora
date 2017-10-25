
from django import template

register = template.Library()

COURSE_FEED_TEMPLATE_NAME_TEMPLATE = "course_feed_{short_title}.html"


@register.inclusion_tag("course_stream_link.html")
def course_stream_link(course):
    return {"course": course}


@register.inclusion_tag("course_mailto_link.html")
def course_mailto_link(course):
    return {"course": course}


@register.inclusion_tag("course_tuwel_link.html")
def course_tuwel_link(course):
    return {"course": course}


@register.simple_tag
def include_course_feed(course):
    template_name = COURSE_FEED_TEMPLATE_NAME_TEMPLATE.format(
                                                short_title=course.short_title)

    try:
        tpl = template.loader.get_template(template_name)
    except template.TemplateDoesNotExist:
        return ""

    return tpl.render()
