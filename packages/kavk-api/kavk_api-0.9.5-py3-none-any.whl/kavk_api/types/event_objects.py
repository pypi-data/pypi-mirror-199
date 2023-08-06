from pydantic import BaseModel as BM
from .objects import MessagesMessage

class ClientInfo(BM):
    button_actions:list[str]
    keyboard:bool
    inline_keyboard:bool
    carousel:bool
    lang_id:int

class MessageNewObject(BM):
    message:MessagesMessage
    client_info:ClientInfo

MessageReplyObject = MessagesMessage

MessageEditObject = MessagesMessage

class MessageAllowObject(BM):
    user_id:int
    key:str

class MessageDenyObject(BM):
    user_id:int

class MessageTypingStateObject(BM):
    state:str
    from_id:int
    to_id:int

class MessageEventObject(BM):
    user_id:int
    peer_id:int
    event_id:str
    payload:str
    conversation_message_id:int

__all__ = ('MessageNewObject', 'MessageReplyObject', 'MessageEditObject', 'MessageAllowObject', 'MessageDenyObject', 'MessageTypingStateObject', 'MessageEventObject')

