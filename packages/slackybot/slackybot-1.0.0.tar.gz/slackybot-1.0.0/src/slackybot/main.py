from .messaging import Message
from .utilities import request_handler, config, helpers
from . import exceptions


class Slack:

    def __init__(self, token=None):
        if not token:
            raise exceptions.SlackInitializeError('Missing token')
        self._token = token
        self._messages = []

    def send_message(self, channel='', text=''):
        """
        Send message to the Slack
        :param channel: (string) Channel name
        :param text: (string) Text message
        :return: (object) SlackMessage
        """
        if output := request_handler.post_request(
            config.data['urls']['post_message'],
            {'channel': channel, 'text': text},
            self._token,
        ):
            if output['ok']:
                slack_message = Message(self._token, channel, text, output)
                self._messages.append(slack_message)
                return slack_message
            else:
                raise helpers.get_exception(output)
        else:
            raise exceptions.MessageNotSend

    def get_messages(self):
        return self._messages[:]
