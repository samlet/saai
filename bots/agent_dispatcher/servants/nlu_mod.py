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
    # 这儿调用的是一个支持多语言的代理服务(也就是nlu_multilang servant), 在一个代理服务之下是多个rasa-nlu工程
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

    # 使用rules对意图进行推断(也就是组合各种inspectors进行判断), 所有的规则都定义在rs_common_*.yml文件中
    prefix = '.'
    kit = RulesetsKit('rasa')
    rs = kit.execute(f"{prefix}/assets/rs_common_{lang_id}.yml",
                     test_intent=None,
                     test_sents=text,
                     show_graph=False)
    resp=kit.as_rasa_format(rs)
    # 如果没有符合条件的意图被推断出来, 则使用rasa-nlu进行意图分类
    ret=resp if resp is not None and len(resp)>0 else invoke_vari(text)
    return json(ret)

