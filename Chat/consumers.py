import json
from channels import Group, Channel
from channels.auth import channel_session_user, channel_session_user_from_http
from datetime import datetime
from django.contrib.auth.models import User

from .models import ChatMessage


def msg_consumer(message):
    room = message.content['room']
    username = message.content['username']
    ChatMessage.objects.create(
        room=room,
        username=username,
        message=message.content['message'],
        post_date=datetime.now()
    )
    Group("chat-%s" % room).send({
        "text": json.dumps({
            "message": message.content['message'],
            "username": username,
        })
    })


@channel_session_user_from_http
def ws_connect(message, room_name):
    message.reply_channel.send({"accept": True})
    message.channel_session['room'] = room_name

    if message.user is not None and not message.user.is_anonymous:
        message.channel_session['username'] = message.user.username
        Group("chat-%s" % room_name).add(message.reply_channel)
    else:
        message.reply_channel.send({"close": True})
        return

    last_messages = ChatMessage.objects.filter(room=room_name).order_by('-post_date')[:3]
    for cm in reversed(last_messages):
        message.reply_channel.send({
            "text": json.dumps({
                "message": cm.message,
                "username": cm.username,
            })
        })


@channel_session_user
def ws_message(message):
    decoded = json.loads(message['text'])
    if decoded['type'] == 'chat-message':
        Channel("chat-messages").send({
            "room": message.channel_session['room'],
            "username": message.channel_session['username'],
            "message": decoded['text'],
        })
    elif decoded['type'] == 'question':
        print('new question: {}'.format(decoded['text']))


@channel_session_user
def ws_disconnect(message):
    room_name = message.channel_session['room']
    Group("chat-%s" % room_name).discard(message.reply_channel)
