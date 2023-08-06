from .base import BotEventType, BaseEvent
from .event_objects import *

class MessageNew(BaseEvent):
    type:BotEventType = BotEventType.MESSAGE_NEW
    object:MessageNewObject


class MessageReply(BaseEvent):
    type:BotEventType = BotEventType.MESSAGE_REPLY
    object:MessageReplyObject


class MessageEdit(BaseEvent):
    type:BotEventType = BotEventType.MESSAGE_EDIT
    object:MessageEditObject


class MessageAllow(BaseEvent):
    type:BotEventType = BotEventType.MESSAGE_ALLOW
    object:MessageAllowObject


class MessageDeny(BaseEvent):
    type:BotEventType = BotEventType.MESSAGE_DENY
    object:MessageDenyObject


class MessageTypingState(BaseEvent):
    type:BotEventType = BotEventType.MESSAGE_TYPING_STATE
    object:MessageTypingStateObject


class MessageEvent(BaseEvent):
    type:BotEventType = BotEventType.MESSAGE_EVENT
    object:MessageEventObject

def get_event(event_type:str):
    try: event = BotEventType(event_type)
    except: return BaseEvent
    if event == BotEventType.MESSAGE_NEW: r = MessageNew
    elif event == BotEventType.MESSAGE_EDIT: r = MessageEdit
    elif event == BotEventType.MESSAGE_DENY: r = MessageDeny
    elif event == BotEventType.MESSAGE_REPLY: r = MessageReply
    elif event == BotEventType.MESSAGE_ALLOW: r = MessageAllow
    elif event == BotEventType.MESSAGE_TYPING_STATE: r = MessageTypingState
    elif event == BotEventType.MESSAGE_EVENT: r = MessageEvent
    else: r = BaseEvent
    return r


__all__ = ('BaseEvent','MessageNew', 'MessageEdit', 'MessageDeny', 'MessageReply', 'MessageAllow', 'MessageTypingState', 'MessageEvent', 'get_event')
