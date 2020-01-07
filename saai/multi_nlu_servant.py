from sanic.response import text
from sanic import Sanic
from sanic import response as res
from sanic.response import json

app = Sanic(__name__)

"""
multi_nlu_servant.py: 兼容rasa-nlu-1.x的http接口的servant
"""

default_return = {
        "intent": {"name": "", "confidence": 0.0},
        "entities": [],
        "text": text,
    }

@app.post('/simulate/<lang_id>/model/parse')
async def post_handler(request, lang_id):
    reqdata=request.json
    print('POST request {} - {}'.format(lang_id, reqdata))
    text=reqdata['text']

    return json(default_return)

@app.post('/nlu/<lang_id>/model/parse')
async def post_handler(request, lang_id):
    from saai.nlu_mod_procs import nlu_mods

    reqdata=request.json
    print('POST request {} - {}'.format(lang_id, reqdata))
    text=reqdata['text']

    resp = await nlu_mods.parse_async(text, lang_id)
    ret=resp if resp is not None and len(resp)>0 else default_return
    return json(ret)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5009)

