from django.conf import settings
from django.db import models
from django.db.models.aggregates import Sum
from django.contrib.auth.models import User
from AuroraUser.models import AuroraUser

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Post(models.Model):
    content = models.TextField('content')
    parent_post = models.ForeignKey('self', null=True, blank=True)
    user = models.ForeignKey(AUTH_USER_MODEL)
    group = models.ForeignKey('Group', null=True, blank=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    filter_group_id = False

    def __unicode__(self):
        return_string = str(self.id) + ' - ' + self.content[0:50]

        if len(self.content) > 50:
            return_string += '...'

        return return_string

    @property
    def sum_votes(self):
        sum_vote = self.postvote_set.aggregate(Sum('value'))
        if sum_vote.get('value__sum'):
            return sum_vote.get('value__sum')
        else:
            return 0

    @property
    def filtered_post_set(self):
        if self.filter_group_id:
            return self.post_set.filter(group_id=self.filter_group_id)
        else:
            return self.post_set

    @property
    def user_avatar(self):
        aurora_user = AuroraUser.objects.get(pk=self.user)
        return aurora_user.avatar


class Thread(models.Model):
    title = models.TextField(max_length=512)
    first_post = models.ForeignKey(Post)
    user = models.ForeignKey(AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    use_group_logic = models.BooleanField(default=False)
    members_in_group = models.IntegerField(default=10)
    filter_group_id = False

    def __unicode__(self):
        return_string = str(self.id) + ' - ' + self.title[0:50]

        if len(self.title) > 50:
            return_string += '...'

        return return_string

    @property
    def filtered_first_post(self):
        filtered_first_post = self.first_post

        if self.filter_group_id:
            filtered_first_post.filter_group_id = self.filter_group_id

        return filtered_first_post


class Favorite(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)


class PostVote(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField()


class Group(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def size(self):
        return self.usergroup_set.count()


class UserGroup(models.Model):
    group = models.ForeignKey(Group)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
