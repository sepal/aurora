import markdown
from markdown.inlinepatterns import LinkPattern, ImagePattern, IMAGE_LINK_RE, LINK_RE

from django_markup.filter import MarkupFilter


class GifferMarkdownFilter(MarkupFilter):
    """
    Applies Markdown conversion to a string, and returns the HTML.
    """
    title = 'Giffer Markdown'

    def render(self, text, **kwargs):
        from markdown import markdown
        return markdown(text, extensions=['diskurs.markdown.giffer:GifferMarkdown'], **kwargs)


class GifferMarkdown(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['image_link'] = GifferImagePattern(IMAGE_LINK_RE, md)
        md.inlinePatterns['link'] = OverrideLinkPattern(LINK_RE, md)


class GifferImagePattern(ImagePattern):
    def handleMatch(self, m):
        node = ImagePattern.handleMatch(self, m)
        src = node.attrib.get('src')

        if src.endswith('.gif'):
            node.attrib.pop('src')
            node.set('data-gifffer', src)
            node.set('data-gifffer-width', '240')

        return node


class OverrideLinkPattern(LinkPattern):
    def handleMatch(self, m):
        node = LinkPattern.handleMatch(self, m)

        node.set('target', '_blank')

        return node
