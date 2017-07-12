from django import template
from django.utils.html import format_html, mark_safe


register = template.Library()


@register.simple_tag
def limit_page(current_page, pg):
    scope = abs(current_page - pg)

    if scope < 3:
        if current_page == pg:
            page_re = """<li >
                            <a style="background-color: #0A5DC3;color: white;border-radius: 3px;">%s</a>
                         </li>""" % pg

        else:
            page_re = """<li>
                            <a href="?page=%s"> %s </a>
                         </li>""" % (pg, pg)

        return format_html(page_re)
    else:
        return ""
