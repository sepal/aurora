
from django import template

register = template.Library()


TUWEL_URL_TEMPLATE = "https://tuwel.tuwien.ac.at/course/view.php?id={tuwel_course_id}"
COURSE_FEED_TEMPLATE_NAME_TEMPLATE = "course_feed_{short_title}.html"


@register.simple_tag
def tuwel_url(course):
    return TUWEL_URL_TEMPLATE.format(tuwel_course_id=course.tuwel_course_id)


@register.simple_tag
def include_course_feed(course):
    template_name = COURSE_FEED_TEMPLATE_NAME_TEMPLATE.format(
                                                short_title=course.short_title)

    try:
        tpl = template.loader.get_template(template_name)
    except template.TemplateDoesNotExist:
        return ""

    return tpl.render()
