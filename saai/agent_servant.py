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
    def __init__(self, conf_file):
        from saai.agent_procs import BotsConf
        self.conf_file=conf_file
        self.conf=BotsConf(conf=self.conf_file)

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
        from saai.agent_procs import BotsConf, handle_message

        data = await request.json()
        sender=request.match_info.get('sender', '_')
        print(data, type(data))
        if not ensure_paras(('mod', 'sents', 'lang'), data):
            # 400 Bad Request
            return web.json_response({
                'error':'invalidate parameters',
                'method': 'handle_message',
                'sender': sender,
                'data': dict(data),
                'headers': dict(request.headers),
            }, status=400, dumps=functools.partial(json.dumps, indent=4))

        # invoke agent
        # handle_message(bot, text, sender='default')
        resp=await handle_message(data['mod'], data['sents'], sender=sender, conf=self.conf)
        return web.json_response(resp, dumps=functools.partial(json.dumps, indent=4))

    async def handle_reload(self, request):
        from saai.agent_procs import get_agent
        data = await request.json()
        # ignore parameter 'model'
        if not ensure_paras(['mod'], data):
            # 400 Bad Request
            return web.json_response({
                'error': 'invalidate parameters',
                'method': 'handle_reload',
                'data': dict(data),
                'headers': dict(request.headers),
            }, status=400, dumps=functools.partial(json.dumps, indent=4))

        mod = data['mod']
        await get_agent(mod, self.conf, force=True)
        resp={mod:'ok'}
        return web.json_response(resp, dumps=functools.partial(json.dumps, indent=4))

    # Notice: 在servant模式下训练nlu模块是有问题的(rasa-1.6), 所以目前不要使用在线训练nlu,
    # 而是通过命令行形式来进行, 如: $ python -m saai.nlu_mod_procs train en
    async def handle_reload_nlu(self, request):
        from saai.nlu_mod_procs import nlu_mods

        data = await request.json()
        # ignore parameter 'model'
        if not ensure_paras(['mod'], data):
            # 400 Bad Request
            return web.json_response({
                'error': 'invalidate parameters',
                'method': 'handle_reload_nlu',
                'data': dict(data),
                'headers': dict(request.headers),
            }, status=400, dumps=functools.partial(json.dumps, indent=4))

        mod = data['mod']
        result=nlu_mods.reload(mod)
        resp={mod:result}
        return web.json_response(resp, dumps=functools.partial(json.dumps, indent=4))

    async def handle_parse(self, request):
        from saai.nlu_mod_procs import nlu_mods
        data = await request.json()
        # ignore parameter 'model'
        if not ensure_paras(('project', 'q'), data):
            # 400 Bad Request
            return web.json_response({
                'error':'invalidate parameters',
                'method': 'handle_parse',
                'data': dict(data),
                'headers': dict(request.headers),
            }, status=400, dumps=functools.partial(json.dumps, indent=4))

        lang=data['project']
        sents=data['q']

        resp =await nlu_mods.parse_async(sents, lang)
        return web.json_response(resp, dumps=functools.partial(json.dumps, indent=4))

    def init(self, loop):
        self.loop = loop
        app = web.Application()
        app.router.add_get('/', self.intro)
        app.router.add_post('/post/{info}', self.post)
        app.router.add_post('/message/{sender}', self.handle_message)
        app.router.add_post('/parse', self.handle_parse)
        app.router.add_post('/reload', self.handle_reload)
        app.router.add_post('/reload_nlu', self.handle_reload_nlu)

        return app

class ServantRunner(object):
    def app(self, conf='agents'):
        """
        $ python -m saai.agent_servant app
        """
        # conf_prefix='/pi/ws/sagas-ai/saai/conf'
        if not conf.startswith('/'):
            conf=f"{conf}.json"
        serv = AgentServ(conf)
        v_loop = asyncio.get_event_loop()
        v_loop.set_debug(True)
        web.run_app(serv.init(v_loop), port=18099)

if __name__ == '__main__':
    import fire
    from sagas.tool.loggers import init_logger

    init_logger()
    fire.Fire(ServantRunner)


