from django.db import models


class ChatMessage(models.Model):
    room = models.TextField()
    message = models.TextField()
    username = models.TextField()
    post_date = models.DateTimeField()


class Question(models.Model):
    text = models.TextField()


class Vote(models.Model):
    UP = True
    DOWN = False
    direction = models.BooleanField(choices=((UP, True), (DOWN, False)),
                                    default=True)
