import nb_log

from ..note import note_blue
from dataclasses import dataclass, field
from quart_schema import validate_request, validate_response
from psycopg2.extras import Json
from utils.redis_manager import RedisMixin, AioRedisManager
import psutil
from quart import websocket
import asyncio
from utils.redis_manager import AioRedisManager
from utils.sqlHelper import PostgresConnectionContextManager
from core.pluginManager import PluginManager
import json


@dataclass
class getNoteListRequest:
    page: int
    pageSize: int
    search: str = ''


@note_blue.get('/getNoteList')
@validate_request(getNoteListRequest)
async def getNoteList(data: getNoteListRequest):
    pass


@dataclass
class openNoteRequest:
    assetId: int


@note_blue.post('/openNote')
@validate_request(openNoteRequest)
async def openNote(data: openNoteRequest):
    # 从note表中获取assetId=data.assetId的记录
    redis = AioRedisManager().get_redis()
    with PostgresConnectionContextManager() as db:
        db.execute('select content,note_id from note where asset_id=%s', (data.assetId,))
        rows = db.fetchone()
        if rows:
            # 遍历content列表将每个元素推入redis
            content = await redis.hget('note', rows[1])
            return {'status': 200, 'data': {"noteId": rows[1], "content": content}}
        else:
            db.execute('insert into note (asset_id,content) values (%s,%s) returning note_id', (data.assetId, Json([])))
            rows = db.fetchone()
            id = rows[0]
        return {'status': 200, 'data': {"noteId": id, "content": {}}}


@dataclass
class saveNoteRequest:
    noteId: int
    content: dict


@note_blue.post('/saveNote')
@validate_request(saveNoteRequest)
async def saveNote(data: saveNoteRequest):
    redis = AioRedisManager().get_redis()
    await redis.hset('note', data.noteId, json.dumps(data.content))
    return {"status": True, "msg": "ok"}


@note_blue.websocket('/syncNote')
async def syncNote():
    redis = AioRedisManager().get_redis()
    while True:
        result = await websocket.receive_json()
        action = result['action']
        if action == 'save':
            noteId = result['noteId']
            content = result['content']
            #       存储在redis中
            await redis.hset('note', noteId, json.dumps(content))
        elif action == 'get':
            noteId = result['noteId']
            content = await redis.hget('note', noteId)
            if content:
                content = json.loads(content)
            else:
                content = {}
            await websocket.send_json({"action": "get", "noteId": noteId, "content": content})
