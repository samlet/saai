from sanic import Blueprint
from sanic.response import json
import requests

info = Blueprint('nlu', url_prefix='/nlu')


@info.route("/ping")
async def ping(request):
    """
    $ curl localhost:1702/info/ping
    :param request:
    :return:
    """
    return json({"hello": "world"})

def invoke_vari(sents, port=5009):
    # url='http://localhost:5005'
    url = f'http://localhost:{port}/nlu/en'
    response = requests.post(f'{url}/model/parse', json={'text': sents})
    print('status code:', response.status_code)
    return response.json()

@info.post('/<lang_id>/model/parse')
async def post_handler(request, lang_id):
    from sagas.kit.rulesets_kit import RulesetsKit

    reqdata=request.json
    print('POST request {} - {}'.format(lang_id, reqdata))
    text=reqdata['text']

    prefix = '.'
    kit = RulesetsKit('rasa')
    rs = kit.execute(f"{prefix}/assets/rs_common_{lang_id}.yml",
                     test_intent=None,
                     test_sents=text,
                     show_graph=False)
    resp=kit.as_rasa_format(rs)
    ret=resp if resp is not None and len(resp)>0 else invoke_vari(text)
    return json(ret)

