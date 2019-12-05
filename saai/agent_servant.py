from aiohttp import web
import textwrap
import asyncio
import functools
import json

import logging

logger = logging.getLogger(__name__)

def ensure_paras(names, paras):
    for name in names:
        if name not in paras:
            return False
    return True

class AgentServ(object):
    async def intro(self, request):
        txt = textwrap.dedent("""\
            Type {url}/hello/John  {url}/simple or {url}/change_body
            in browser url bar
        """).format(url='127.0.0.1:18099')
        binary = txt.encode('utf8')
        resp = web.StreamResponse()
        resp.content_length = len(binary)
        resp.content_type = 'text/plain'
        await resp.prepare(request)
        await resp.write(binary)
        return resp

    async def post(self, request):
        """
        POST - http://localhost:18099/post/path
        body(json) - {"x":5}
        :param request:
        :return:
        """
        data = await request.json()
        info=request.match_info.get('info', '_')
        print(data, type(data))
        return web.json_response({
            'method': 'post',
            'info': info,
            # 'args': dict(request.GET),
            'data': dict(data),
            'headers': dict(request.headers),
        }, dumps=functools.partial(json.dumps, indent=4))

    async def handle_message(self, request):
        """
        POST - http://localhost:18099/message/sender_id
        body(json) - {"x":5}
        :param request:
        :return:
        """
        from saai.agent_procs import handle_message

        data = await request.json()
        sender=request.match_info.get('sender', '_')
        print(data, type(data))
        if not ensure_paras(('mod', 'sents', 'lang'), data):
            return web.json_response({
                'error':'invalidate parameters',
                'method': 'handle_message',
                'sender': sender,
                'data': dict(data),
                'headers': dict(request.headers),
            }, dumps=functools.partial(json.dumps, indent=4))

        # invoke agent
        # handle_message(bot, text, sender='default')
        resp=await handle_message(data['mod'], data['sents'], sender=sender)
        return web.json_response(resp, dumps=functools.partial(json.dumps, indent=4))

    def init(self, loop):
        self.loop = loop
        app = web.Application()
        app.router.add_get('/', self.intro)
        app.router.add_post('/post/{info}', self.post)
        app.router.add_post('/message/{sender}', self.handle_message)

        return app

if __name__ == '__main__':
    """
    $ python -m saai.agent_servant
    """
    serv=AgentServ()
    v_loop = asyncio.get_event_loop()
    v_loop.set_debug(True)
    web.run_app(serv.init(v_loop), port=18099)

