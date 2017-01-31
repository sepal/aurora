from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import re

from Course.models import Course


class SlideStack(models.Model):
    """
    A SlideStacks is a "container" for slides. It manages a set of slides of the same affiliation.
    """
    title           = models.CharField(max_length=120)
    slug            = models.SlugField(unique=True, blank=True)
    pub_date        = models.DateTimeField(default=timezone.now)
    tags            = models.CharField(max_length=240, blank=True, null=True)
    categories      = models.TextField(max_length=500, blank=True, null=True)
    course          = models.ForeignKey(Course)

    @property
    def slides(self):
        """
        :return: a filter set of Slides, assigned to this SlideStack.
        """
        return Slide.objects.filter(slide_stack=self)

    @property
    def list_categories(self):
        """
        :return: a list of categories. Each element looks like follows: "Category_Topic"
        """
        if self.categories is not None:
            return [x.strip() for x in self.categories.split(',')]
        return []

    @property
    def list_category_tuples(self):
        """
        same method like list_categories() but return format is different.
        :return: a list of tuples. A tuple looks like follows: (Category, Topic)
        """
        if self.categories is not None:
            list_categories = [x.strip() for x in self.categories.split(',')]
            category_tuples = []
            for cat in list_categories:
                if not cat == '':
                    category_tuples.append(cat.split('_'))

            return category_tuples

        return []

    def __str__(self):
        return self.title

    def __repr__(self):
        return repr(self.id)

    def save(self, **kwargs):
        unique_slugify(self, self.title)
        super(SlideStack, self).save(**kwargs)


class Slide(models.Model):
    """
    This class represents a single slide. Each slide has a set of variables and is assigned to exactly one SlideStack.
    """
    def upload_location(instance, filename):
        return "slides/%s/%s" % (instance.slide_stack.slug, filename)

    title           = models.CharField(max_length=120)
    image           = models.ImageField(upload_to=upload_location)
    text_content    = models.TextField(blank=True, null=True)
    tags            = models.CharField(max_length=240, blank=True, null=True)
    slide_stack     = models.ForeignKey(SlideStack)

    def __str__(self):
        return self.title


def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
                   slug_separator='-'):
    """
    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len-len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator='-'):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value