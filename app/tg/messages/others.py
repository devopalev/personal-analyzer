from app.tg.messages.base import MessageTextSimpleBuilder


class MassageEventError(MessageTextSimpleBuilder):
    key = "/event/error"


class MassageCommandStart(MessageTextSimpleBuilder):
    key = "/commands/start"


class MassageCommandHelp(MessageTextSimpleBuilder):
    key = "/commands/help"
