from quart import Quart, render_template, request, redirect, url_for, session, Response, websocket
from quart_schema import QuartSchema
from api.project import project_blue
from api.tags import tag_blue
from api.service import service_blue
from quart_cors import cors
from utils.redis_manager import AioRedisManager
from core.notify import Notify
import json


app = Quart(__name__)
app = cors(app, allow_origin='*')
app.register_blueprint(project_blue)
app.register_blueprint(tag_blue)
app.register_blueprint(service_blue)
QuartSchema(app)
# redis = RedisMixin().redis_db_service
redis = AioRedisManager().get_redis()
@app.before_request
async def handle_options():
    if request.method == 'OPTIONS':
        return Response(status=200)



@app.websocket('/ws')
async def ws():
    '''
    webscoket实时通知，获取redis队列中的消息。减少轮询造成的压力
    :return:
    '''
    await websocket.send('hello')
    while True:
        msg = await redis.blpop('notify', 30)
        if msg:
            await websocket.send(msg[1])
        else:
            await websocket.send('heartbeat')




# 解决跨域问题


if __name__ == '__main__':

    from plugins import importPlugins

    importPlugins()
    app.run(port=5000)
