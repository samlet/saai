from sanic import Blueprint
from sanic.response import json

info = Blueprint('info', url_prefix='/info')


@info.route("/ping")
async def ping(request):
    """
    $ curl localhost:1701/info/ping

    :param request:
    :return:
    """
    return json({"hello": "world"})

@info.post('/event/<lang>')
async def handle_event(request, lang):
    """
    $ curl -s -d '{"sents":"I want to play music."}' \
        -H "Content-Type: application/json" -X POST \
        localhost:1701/info/event/en | json
    $ curl -s -d '{"sents":"how about north eastern food?"}' \
        -H "Content-Type: application/json" -X POST \
        localhost:1701/info/event/en | json
    :param request:
    :param lang:
    :return:
    """
    from sagas.kit.rulesets_kit import RulesetsKit
    from sagas.nlu.inspector_registry import ci
    from pprint import pprint
    rd = request.json
    sents = rd['sents']
    rs = RulesetsKit().execute(f"./assets/rs_common_{lang}.yml",
                               test_intent=None,
                               test_sents=sents,
                               show_graph=False)
    pprint(rs)
    return json(rs)

