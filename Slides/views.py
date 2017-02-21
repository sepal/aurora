from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404

from operator import attrgetter
from django.utils import timezone

# Create your views here.
from AuroraProject.decorators import aurora_login_required
from .models import Slide, SlideStack
from .structures import GsiStructure, GsiDataStructure, HciStructure, HciDataStructure
from Course.models import Course


@aurora_login_required()
def slides(request, course_short_title=None):
    """
    :param request:
    :return: a view of all categories and their assigned topics.
    """
    data_structure = []
    if course_short_title == 'gsi':
        data_structure = GsiDataStructure.data_structure
    elif course_short_title == 'hci':
        data_structure = HciDataStructure.data_structure

    print(timezone.now())
    context = {
        "structure": data_structure,
        "course": Course.get_or_raise_404(course_short_title),
    }
    return render(request, "slides_overview.html", context)


@aurora_login_required()
def slide_topics(request, topic=None, course_short_title=None):
    """
    :param request:
    :param topic: the topic to be represented
    :return: shows all SlideStacks, which are assigned to the given topic.
    """

    # search for all slideStacks assigned to the topic
    used_slide_stacks = list()
    for ss in SlideStack.objects.filter(course=Course.objects.get(short_title=course_short_title)):
        if topic.lower() in (x.lower() for x in ss.list_categories):
            used_slide_stacks.append(ss)

    # check date
    filter_future_dates(used_slide_stacks)

    complete_list = sort_list_by_id(used_slide_stacks)

    # create next and previous link
    structure = list()
    if course_short_title == 'gsi':
        structure = GsiStructure.structure
    elif course_short_title == 'hci':
        structure = HciStructure.structure

    tup = topic.split('_')
    prev = ''
    nxt = ''
    for lst in structure:
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
        "section": tup[0],
        "used_slide_stacks": complete_list,
        "prev": prev,
        "nxt": nxt,
        "top": topic,
        "course": Course.get_or_raise_404(course_short_title),
    }

    return render(request, "slide_topics.html", context)


@aurora_login_required()
def slide_stack(request, topic=None, slug=None, course_short_title=None):
    """
    :param request:
    :param topic: defines the context. This is important for previous and next page functionality.
    :param slug: identifies the SlideStack to be displayed.
    :return: a view of all slides assigned to the SlideStack.
    """

    this_ss = get_object_or_404(SlideStack, slug=slug)

    # check date
    if this_ss.pub_date > timezone.now():
        raise Http404("No such slide collection exists, or is published yet")

    # create next and previous link
    prev = ''
    nxt = ''
    if topic != 'none':
        ind = -1
        stop = False
        used_slide_stacks = list()
        for ss in SlideStack.objects.filter(course=Course.objects.get(short_title=course_short_title)):
            if topic.lower() in (x.lower() for x in ss.list_categories):
                used_slide_stacks.append(ss)

                if stop:
                    break

                if ss.slug == slug:
                    ind = len(used_slide_stacks) - 1
                    stop = True

        if ind > 0:
            nxt = reverse("Slides:slidestack", kwargs={"topic": topic, "slug": used_slide_stacks[ind - 1].slug,
                                                        "course_short_title": course_short_title})
        if ind < len(used_slide_stacks) - 1:
            prev = reverse("Slides:slidestack", kwargs={"topic": topic, "slug": used_slide_stacks[ind + 1].slug,
                                                       "course_short_title": course_short_title})

    # find all other topics containing this SlideStack
    other_topics = []
    this_topic = ('','search results')
    for cat in this_ss.list_category_tuples:
        if topic != cat[0] + '_' + cat[1]:
            other_topics.append(cat)
        else:
            this_topic = cat

    context = {
        "slide_stack": this_ss,
        "other_topics": other_topics,
        "prev": prev,
        "nxt": nxt,
        "this_topic": this_topic, 
        "course": Course.get_or_raise_404(course_short_title),
    }

    return render(request, "slide_stack.html", context)


@aurora_login_required()
def search(request, course_short_title=None):
    """
    Searches all SlideStacks and Slides for the given text
    :param request:
    :return: a view of all SlideStacks, which contain the search text
    in a variable, or has a Slide assigned that fits the search criteria.
    """

    query = request.GET.get("q")
    if query:

        # if query == 'register new slides'

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

        complete_set = set(queryset_ss)
        for slide in queryset_slides:
            complete_set.add(slide.slide_stack)

        # filter for course
        course_filtered_list = []
        for item in complete_set:
            if item.course.short_title == course_short_title:
                course_filtered_list.append(item)

        # check date
        filter_future_dates(course_filtered_list)

        complete_list = sort_list_by_id(course_filtered_list)

        title = 'nothing found'
        if len(complete_list) != 0:
            title = 'results found:'

    context = {
        "title": title,
        "found_slides": complete_list,
        "course": Course.get_or_raise_404(course_short_title),
    }

    return render(request, "search.html", context)


@aurora_login_required()
def refresh_structure(request, course_short_title=None):
    """
    This view refreshes the data structure for slide stacks.
    Can only be performed by authorized staff.
    :param request:
    :param course_short_title:
    :return:
    """
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404("You are not authorized for this action!")

    print('data structure will be redefined')
    GsiDataStructure.redefine_data_structure()
    HciDataStructure.redefine_data_structure()

    return slides(request, course_short_title=course_short_title)

    # # not working ?!?
    # return render(request, "redefine_data_structure.html", {"course": Course.get_or_raise_404(course_short_title),})


def filter_future_dates(slide_stack_list):
    """
    filters the SlideStack list for entries not published yet
    :param slide_stack_list: list of SlideStacks to be filtered
    :return: filtered list
    """
    for ss in slide_stack_list:
        if ss.pub_date > timezone.now():
            slide_stack_list.remove(ss)

    return slide_stack_list


def sort_list_by_id(slide_stack_list):
    """
    orders the SlideStack list by id
    :param slide_stack_list: list to be ordered
    :return: ordered list by id
    """
    sorted_list = sorted(slide_stack_list, key=attrgetter('id'), reverse=False)

    return sorted_list

