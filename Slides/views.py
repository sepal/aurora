from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.db.models import Q

from operator import attrgetter


# Create your views here.
from .models import Slide, SlideStack, Structure, DataStructure
from Course.models import Course


def slides(request, course_short_title=None):
    """
    :param request:
    :return: a view of all categories and their assigned topics.
    """

    context = {
        "structure": DataStructure.data_structure,
        "course": Course.get_or_raise_404(course_short_title),
    }
    return render(request, "slides_overview.html", context)


def slide_topics(request, topic=None, course_short_title=None):
    """
    :param request:
    :param topic: the topic to be represented
    :return: shows all SlideStacks, which are assigned to the given topic.
    """

    used_slide_stacks = []
    for ss in SlideStack.objects.all():
        if topic.lower() in (x.lower() for x in ss.list_categories):
            used_slide_stacks.append(ss)

    # create next and previous link
    tup = topic.split('_')
    prev = ''
    nxt = ''
    for lst in Structure.structure:
        if lst[0] == tup[0]:
            chapt = lst.pop(0)
            i = lst.index(tup[1])
            if i > 0:
                prev = '../' + chapt + '_' + lst[i - 1]
            if len(lst) > i + 1:
                nxt = '../' + chapt + '_' + lst[i + 1]
            lst.insert(0, chapt)

    context = {
        "title": tup[1],
        "used_slide_stacks": used_slide_stacks,
        "prev": prev,
        "nxt": nxt,
        "top": topic,
        "course": Course.get_or_raise_404(course_short_title),
    }

    return render(request, "slide_topics.html", context)


def slide_stack(request, topic=None, slug=None, course_short_title=None):
    """
    :param request:
    :param topic: defines the context. This is important for previous and next page functionality.
    :param slug: identifies the SlideStack to be displayed.
    :return: a view of all slides assigned to the SlideStack.
    """

    this_ss = get_object_or_404(SlideStack, slug=slug)

    # create next and previous link
    prev = ''
    nxt = ''
    if topic != 'none':
        ind = -1
        stop = False
        used_slide_stacks = []
        for ss in SlideStack.objects.all():
            if topic.lower() in (x.lower() for x in ss.list_categories):
                used_slide_stacks.append(ss)

                if stop:
                    break

                if ss.slug == slug:
                    ind = len(used_slide_stacks) - 1
                    stop = True

        if ind > 0:
            prev = reverse("Slides:slidestack", kwargs={"topic": topic, "slug": used_slide_stacks[ind - 1].slug,
                                                        "course_short_title": course_short_title})
        if ind < len(used_slide_stacks) - 1:
            nxt = reverse("Slides:slidestack", kwargs={"topic": topic, "slug": used_slide_stacks[ind + 1].slug,
                                                       "course_short_title": course_short_title})

    # find all other topics containing this SlideStack
    other_topics = []
    for cat in this_ss.list_category_tuples:
        if topic != cat[0] + '_' + cat[1]:
            other_topics.append(cat)

    context = {
        "title": this_ss.title,
        "other_topics": other_topics,
        "slides": this_ss.slides,
        "prev": prev,
        "nxt": nxt,
        "course": Course.get_or_raise_404(course_short_title),
    }

    return render(request, "slide_stack.html", context)


def search(request, course_short_title=None):
    """
    Searches all SlideStacks and Slides for the given text
    :param request:
    :return: a view of all SlideStacks, which contain the search text
    in a variable, or has a Slide assigned that fits the search criteria.
    """

    title = 'nothing found'

    query = request.GET.get("q")
    if query:
        queryset_ss = SlideStack.objects.filter(
            Q(title__icontains=query) |
            Q(tags__icontains=query) |
            Q(categories__icontains=query)
        ).distinct()

        queryset_slides = Slide.objects.filter(
            Q(title__icontains=query) |
            Q(text_content__icontains=query) |
            Q(tags__icontains=query)
        ).distinct()

        if queryset_slides or queryset_ss:
            title = 'results found:'

        complete_set = set(queryset_ss)
        for slide in queryset_slides:
            complete_set.add(slide.slide_stack)

        complete_list = sorted(complete_set, key=attrgetter('id'), reverse=False)

    context = {
        "title": title,
        "found_slides": complete_list,
        "course": Course.get_or_raise_404(course_short_title),
    }

    return render(request, "search.html", context)
