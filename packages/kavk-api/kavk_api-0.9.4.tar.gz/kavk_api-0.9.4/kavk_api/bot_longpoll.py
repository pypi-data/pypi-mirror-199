from .kavk_api import Vk
from .types.base import BotEventType
from .types.events import EVENTS
from .utils import DotDict

class BotEvent:
    def __init__(self, raw:dict) -> None:
        self.raw = raw
        self.type = raw.get('type', 'undefined_type') # Если не находим raw['type'] возвращаем undefined_type
        if self.type in [i.value for i in BotEventType]: # Проверка есть ли наш тип в BotEventType 
            self.type = BotEventType(self.type) # Если есть преобразуем
        self.object = raw.get('object', {})
        if isinstance(self.type, BotEventType) and self.type in EVENTS.keys() and self.object != {}:
            self.object = EVENTS[self.type](**self.object)
        else: self.object = DotDict(self.object)


class BotLongPoll:
    def __init__(self, vk:Vk, wait:int=25, mode:int=2, v:int=3) -> None:
        self._vk = vk
        self._api = vk.get_api()
        self._wait = wait
        self._mode = mode
        self._v = v
        self.params = {}
        self.updates = []

    async def listen(self):
        while 1:
            async for event in BotLongPoll(self._vk, self._wait, self._mode, self._v):
                yield event
    
    async def get_event(self, url:str, params:dict) -> dict:
        r = await self._vk.client.get(url=url, params=params)
        r = await r.json()
        return r

    # Что происходит дальше?
    # __aiter__ возвращает коду `async for e in LongPoll.listem()`
    # функцию __anext__.
    # Она же в свою очередь просто получает наш новый ивент

    def __aiter__(self): return self

    async def __anext__(self) -> BotEvent:
        if self.params == {}: 
            group_id = await self._api.groups.getById()
            group_id = group_id[0].id
            r = await self._api.groups.getLongPollServer(group_id=group_id)
            self.params:dict = {'key': r.key, 'ts': r.ts,
                           'wait': self._wait, 'mode': self._mode,
                           'version': self._v, 'act': 'a_check'}
            self.server:str = r.server

        if self.updates != []:
            u = self.updates.pop(0)
            return BotEvent(u)
            
        r = await self.get_event(url=self.server, params=self.params)
        try:
            updates = r['updates']
        except IndexError:
            error = r['failed']
            if error == 1:
                self.params.update({'ts': r['ts']})
            elif error in (2,3):
                self.params = {}
            updates = [{'type': ''}]
        except Exception as e:
            raise e

        if len(updates) > 0:
            self.updates = updates[1:]
            update = updates[0]
        elif updates == []:
            update = {'type': ''}
        else: update:dict = updates[0]
        self.params.update({'ts': r['ts']})
        return BotEvent(update)

__all__ = ("BotLongPoll", "BotEvent", 'BotEventType')
