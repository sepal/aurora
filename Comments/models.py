from django.db import models as models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Q, Count, Max
import re
from taggit.managers import TaggableManager
from memoize import memoize

class CommentList(models.Model):
    """
    currently Comments are associated with CommentList only by having the same reference object
    (i.e. object_id/content_type and content_object are identical)
    """

    revision = models.BigIntegerField(default=0)
    uri = models.CharField(max_length=200, null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('content_type', 'object_id')

    @staticmethod
    def get_or_create(ref_object):
        ref_type = ContentType.objects.get_for_model(ref_object)

        try:
            revision = CommentList.objects.get(
                content_type__pk=ref_type.id,
                object_id=ref_object.id)
        except CommentList.DoesNotExist:
            revision = CommentList.objects.create(content_object=ref_object)

        return revision

    @staticmethod
    def get_by_ref_numbers(ref_id, ref_type):
        try:
            comment_list = CommentList.objects.get(
                content_type__pk=ref_type,
                object_id=ref_id)
        except CommentList.DoesNotExist:
            ref_obj = Comment.ref_id_type_to_obj(ref_id, ref_type)
            comment_list = CommentList.objects.create(content_object=ref_obj)

        return comment_list

    @staticmethod
    def get_by_comment(comment):
        return CommentList.get_by_ref_numbers(comment.object_id,
                                              comment.content_type.id)

    def increment(self):
        self.revision += 1
        self.save()


class Vote(models.Model):
    UP = True
    DOWN = False
    direction = models.BooleanField(choices=((UP, True), (DOWN, False)),
                                    default=True)

    voter = models.ForeignKey('AuroraUser.AuroraUser', on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', related_name='votes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('voter', 'comment')


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey('AuroraUser.AuroraUser', on_delete=models.CASCADE)
    post_date = models.DateTimeField('date posted')
    delete_date = models.DateTimeField('date deleted', blank=True, null=True)
    edited_date = models.DateTimeField('date edited', blank=True, null=True)
    deleter = models.ForeignKey('AuroraUser.AuroraUser',
                                related_name='deleted_comments_set',
                                blank=True, null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', blank=True, null=True,
                               related_name='children', on_delete=models.CASCADE)
    promoted = models.BooleanField(default=False)
    tags = TaggableManager()
    seen = models.BooleanField(default=False)

    # Foreign object this Comment is attached to
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    PUBLIC = 'public'
    STAFF = 'staff'
    PRIVATE = 'private'
    VISIBILITY_CHOICES = (
        (PUBLIC, 'public'),
        (STAFF, 'staff only'),
        (PRIVATE, 'private note')
    )

    visibility = models.CharField(max_length=10,
                                  choices=VISIBILITY_CHOICES,
                                  default=PUBLIC)

    bookmarked_by = models.ManyToManyField('AuroraUser.AuroraUser',
                                           related_name='bookmarked_comments_set')

    def save(self, *args, **kwargs):
        super(Comment, self).save(*args, **kwargs)
        self.set_tags_from_text()

    @property
    # @memoize(timeout=5)
    def score(self):
        up_votes = self.votes.filter(direction=Vote.UP).count()
        down_votes = self.votes.filter(direction=Vote.DOWN).count()
        return up_votes - down_votes

    # @memoize(timeout=5)
    def responses(self):
        responses = self.children.order_by('post_date')
        responses = Comment.filter_visible(responses, self.requester)
        Comment.set_flags(responses, self.requester)
        return responses

    def __str__(self):
        return str(self.id) + ": " + self.text[:30]

    def __unicode__(self):
        return str(self.id) + ": " + self.text[:30]

    def set_tags_from_text(self):
        tag_pattern = '#[\S]+'
        tags = re.findall(tag_pattern, self.text)
        tags = [tag.lower() for tag in tags]
        self.tags.add(*tags)

    def thread_seen(self):
        if not self.seen:
            return False
        for child in self.children.all():
            if not child.seen:
                return False
        return True

    @staticmethod
    def query_tagged(tags):
        return Comment.objects.filter(tags__name__in=tags)

    @staticmethod
    def get_points_for_user(user):
        return Comment.objects.filter(author=user, promoted=True).count()

    @staticmethod
    def query_top_level_sorted(ref_object_id, ref_type_id, requester,
                               newest_last=False):
        queryset_all = Comment.objects.filter(
            parent=None,
            content_type__pk=ref_type_id,
            object_id=ref_object_id)

        visible = Comment.filter_visible(queryset_all, requester)
        visible = Comment.filter_deleted_trees(visible)
        if newest_last:
            visible = visible.order_by('post_date')
        else:
            visible = visible.order_by('-post_date')

        # Only when all query actions are done we can set custom properties to
        # the objects in the queryset. If another query method is called (even if
        # it's just order_by() the Instances and their custom non persistent properties
        # will be overwritten.

        Comment.set_flags(visible, requester)
        return visible

    @staticmethod
    def query_all(ref_object_id, ref_type_id, requester):
        queryset = Comment.objects.filter(
            content_type__pk=ref_type_id,
            object_id=ref_object_id)

        visible_comments = Comment.filter_visible(queryset, requester)
        Comment.set_flags(visible_comments, requester)
        return visible_comments

    @staticmethod
    def query_number_of_all(ref_object_id, ref_type_id, requester):
        queryset = Comment.query_all(ref_object_id, ref_type_id, requester)
        return queryset.filter(deleter=None).count()

    @staticmethod
    def query_bookmarks(requester):
        result = requester.bookmarked_comments_set.all().order_by('-post_date')
        Comment.filter_visible(result, requester)
        Comment.set_flags(result, requester)
        return result

    # @staticmethod
    # def set_bookmark_flags(comment_set, requester):
    #     for comment in comment_set:
    #         comment.bookmarked = True if comment.bookmarked_by.filter(pk=requester.id).exists() else False
    #         comment.requester = requester

    @staticmethod
    # @memoize(timeout=5)
    def set_flags(comment_set, requester):
        for comment in comment_set:
            comment.requester = requester
            # comment.set_visibility_flag(requester)
            comment.bookmarked = True if comment.bookmarked_by.filter(
                pk=requester.id).exists() else False

            comment.uri = CommentList.get_by_comment(comment).uri

            try:
                vote = Vote.objects.get(comment=comment, voter=requester)
                comment.voted = 'upvoted' if vote.direction == vote.UP else 'downvoted'
            except Vote.DoesNotExist:
                comment.voted = ''

    def set_visibility_flag(self, requester):
        self.visible = False
        if self.visibility == Comment.PUBLIC:
            self.visible = True
            return

        if self.author == requester:
            self.visible = True
            return

        if self.visibility == Comment.STAFF and requester.is_staff:
            self.visibility = True
            return

        if self.parent.author == requester:
            self.visibility = True
            return

    # TODO not working for some weird reason
    # TODO delete or fix
    @staticmethod
    def set_permission_flags(comment_set, requester):
        for comment in comment_set:
            if comment.author == requester or requester.is_staff:
                comment.editable = True
                comment.deletable = True

            if comment.deleter is not None:
                comment.deletable = False

    @staticmethod
    def filter_deleted_trees(comment_set):
        # for every deleted parent
        for comment in comment_set.exclude(deleter=None):
            # if not deleted responses <= 0
            if comment.children.filter(deleter=None).count() <= 0:
                # remove parent from queryset
                comment_set = comment_set.exclude(id=comment.id)

        return comment_set

    @staticmethod
    def filter_visible(queryset, requester):
        non_private_or_authored = queryset.filter(
            ~Q(visibility=Comment.PRIVATE) | Q(author=requester))
        if requester.is_staff:
            return non_private_or_authored

        return non_private_or_authored.filter(
            ~Q(visibility=Comment.STAFF) | Q(author=requester))

    @staticmethod
    def ref_obj_to_id_type(ref_object):
        ref_type = ContentType.objects.get_for_model(ref_object)
        return ref_object.id, ref_type.id

    @staticmethod
    def ref_id_type_to_obj(ref_id, ref_type):
        ref_obj_model = ContentType.objects.get_for_id(ref_type).model_class()
        return ref_obj_model.objects.get(id=ref_id)

    @staticmethod
    def count_for(content_type_name, content_id, is_staff=False):
        """
        Returns number of comments for the given content_type and content_id
        without private notes.

        :param content_type_name:
           The name of your model as a string, e.g. issue or stack
        :param content_id:
           The id of the object, to which the comments are attached to.
        :param is_staff:
            True if the count should include notes visible to staff only. False
            by default.
        :return:
            An integer representing the number of comments.
        """
        visibility = [Comment.PUBLIC]
        if is_staff:
            visibility.append(Comment.STAFF)
        content_types = ContentType.objects.filter(name=content_type_name)
        if len(content_types) > 0:
            return Comment.objects.filter(content_type=content_types[0],
                                          object_id=content_id,
                                          delete_date=None,
                                          visibility__in=visibility).count()
        # todo: raise an error instead?
        return 0


class CommentsConfig(models.Model):
    key = models.CharField(primary_key=True, max_length=30)
    value = models.CharField(max_length=20)

    factor = 1000

    @staticmethod
    def setup():
        CommentsConfig.objects.create(key='polling_active',
                                      value='5')
        CommentsConfig.objects.create(key='polling_idle',
                                      value='60')

    @staticmethod
    def get_polling_interval():
        active = CommentsConfig.objects.get(key='polling_active')
        idle = CommentsConfig.objects.get(key='polling_idle')

        return int(active.value) * CommentsConfig.factor, int(
            idle.value) * CommentsConfig.factor

    def __unicode__(self):
        return self.key

    def __str__(self):
        return self.key


class CommentReferenceObject(models.Model):
    """
    If there is no other Object available this Model can be used to create
    reference Objects. Comments can then be attached to that reference Object.
    """

    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        name = '' if self.name is None else ': ' + self.name
        return str(self.id) + self.name

    def __str__(self):
        name = '' if self.name is None else ': ' + self.name
        return str(self.id) + self.name
