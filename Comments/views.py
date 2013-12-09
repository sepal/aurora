from django.core.urlresolvers import reverse
from django.shortcuts import render

from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django import forms
from django.utils import timezone
from django.http import HttpResponseRedirect

from Comments.models import Comment
from PortfolioUser.models import PortfolioUser


class CommentList(ListView):
    #queryset = Comment.objects.order_by('-post_date')
    queryset = Comment.objects.filter(parent=None).order_by('-post_date')

    def get_context_data(self, **kwargs):
        context = super(CommentList, self).get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['form_action'] = '/post/'
        return context


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='')


# TODO do some more reading on csrf protection, maybe use csrf required decorator
@login_required
def post_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            user = PortfolioUser.objects.filter(id=request.user.id)[0]
            # TODO authentication + authorization?!
            comment = Comment.objects.create(text=form.cleaned_data['text'], author=user, post_date=timezone.now())
            comment.save()
    return HttpResponseRedirect(reverse('Comments:feed'))