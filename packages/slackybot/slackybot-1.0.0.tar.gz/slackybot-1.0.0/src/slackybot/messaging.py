from .utilities import request_handler, config, helpers
from . import exceptions
import uuid


class SlackMessage:

    def __init__(self, token, channel, text, data):
        self.id = str(uuid.uuid4())[:13].replace('-', '')
        self._token = token
        self._ts = data['ts']
        self._channel = data['channel']
        self._deleted = False

        self.channel = channel
        self.text = text

    def __srt__(self):
        return f'<{self.__class__.__name__} {self.id}>'

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'

    def update(self, text=''):
        if output := request_handler.post_request(
                config.data['urls']['update_message'],
                {'channel': self._channel, 'ts': self._ts, 'text': text},
                self._token,
        ):
            if output['ok']:
                self.text = text
            else:
                raise helpers.get_exception(output)
        else:
            raise exceptions.MessageNotUpdated

    def delete(self):
        if self._deleted:
            raise exceptions.MessageAlreadyDeleted

        if output := request_handler.post_request(
                config.data['urls']['delete_message'],
                {'channel': self._channel, 'ts': self._ts},
                self._token,
        ):
            if output['ok']:
                self._deleted = True
            else:
                raise helpers.get_exception(output)
        else:
            raise exceptions.MessageNotDeleted


class Message(SlackMessage):

    def __init__(self, token, channel, text, data):
        super().__init__(token, channel, text, data)
        self._replies = []

    def send_reply(self, text=''):
        if output := request_handler.post_request(
                config.data['urls']['post_message'],
                {'channel': self.channel, 'thread_ts': self._ts, 'text': text},
                self._token,
        ):
            if output['ok']:
                reply = Reply(self._token, self.channel, text, output)
                self._replies.append(reply)
                return reply
            else:
                raise helpers.get_exception(output)
        else:
            raise exceptions.MessageNotSend

    def get_replies(self):
        return self._replies[:]


class Reply(SlackMessage):
    pass
