import os
from django import template

from Elaboration.models import Elaboration
from FileUpload.models import UploadFile

register = template.Library()


@register.inclusion_tag('elaboration_files.html', takes_context=True)
def render_uploads(context, elaboration):
    elaboration = Elaboration.objects.get(id=elaboration.id)
    files = []
    index = 0
    for upload_file in UploadFile.objects.filter(user=elaboration.user, elaboration__id=elaboration.id).order_by('creation_time'):
        index += 1
        file_map = file_map_for_upload(upload_file, index, elaboration)
        files.append(file_map)

    context.update({'files': files})
    return context


def file_map_for_upload(upload_file, index, elaboration):
    if not os.path.isfile(upload_file.upload_file.name):
        file_map = {'name': "Placeholder",
                    'size': "0",
                    'url': "https://placeimg.com/640/480/any",
                    'thumbnail_url': "https://placeimg.com/300/300/any",
                    'accepted_files': elaboration.challenge.accepted_files}
    else:
        file_map = {'name': os.path.basename(upload_file.upload_file.name),
                    'size': round((upload_file.upload_file.size / 1048576), 2),
                    'url': upload_file.upload_file.url,
                    'thumbnail_url': upload_file.thumbnail.url,
                    'accepted_files': elaboration.challenge.accepted_files}
        if 'pdf' not in elaboration.challenge.accepted_files:
            figure = 'Fig. ' + str(index)
            file_map['fig'] = figure

    return file_map


@register.inclusion_tag('elaboration_files.html', takes_context=True)
def render_original_uploads(context, elaboration):
    elaboration = Elaboration.objects.get(id=elaboration.id)
    files = []
    index = 0
    for upload_file in UploadFile.objects.filter(user=elaboration.user, elaboration__id=elaboration.id, elaboration_version='original').order_by('creation_time'):
        index += 1
        file_map = file_map_for_upload(upload_file, index, elaboration)
        files.append(file_map)

    context.update({'files': files})
    return context


@register.inclusion_tag('elaboration_files.html', takes_context=True)
def render_revised_uploads(context, elaboration):
    elaboration = Elaboration.objects.get(id=elaboration.id)
    files = []
    index = 0
    for upload_file in UploadFile.objects.filter(user=elaboration.user, elaboration__id=elaboration.id, elaboration_version='revision').order_by(
            'creation_time'):
        index += 1
        file_map = file_map_for_upload(upload_file, index, elaboration)
        files.append(file_map)
    context.update({'files': files})
    return context
