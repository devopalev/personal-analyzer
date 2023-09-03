from app.tg.messages.base import MessageTextSimpleBuilder


class MassageEventError(MessageTextSimpleBuilder):
    _key_message_text = "/event/error"


class MassageCommandStart(MessageTextSimpleBuilder):
    _key_message_text = "/commands/start"


class MassageCommandHelp(MessageTextSimpleBuilder):
    _key_message_text = "/commands/help"
