from pydantic import BaseModel
from .base import BotEventType
from .objects import MessagesMessage

class ClientInfo(BaseModel):
    button_actions:list[str]
    keyboard:bool
    inline_keyboard:bool
    carousel:bool
    lang_id:int

class MessageNewObject(BaseModel):
    message:MessagesMessage
    client_info:ClientInfo

EVENTS = {BotEventType.MESSAGE_NEW:MessageNewObject}

__all__ = ('EVENTS', 'MessageNewObject')
