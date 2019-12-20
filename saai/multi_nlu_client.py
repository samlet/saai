from rasa.core.trackers import DialogueStateTracker
from rasa.core.interpreter import RasaNLUHttpInterpreter
from rasa.utils.endpoints import EndpointConfig
from rasa.core.slots import Slot
from pprint import pprint

DEFAULT_SERVER_PORT = 5008
DEFAULT_SERVER_FORMAT = "{}://localhost:{}"
DEFAULT_SERVER_URL = DEFAULT_SERVER_FORMAT.format("http", DEFAULT_SERVER_PORT)

async def nlu_parse(url, message):
    tracker = DialogueStateTracker.from_dict("1", [], [Slot("requested_language")])
    # we'll expect this value 'en' to be part of the result from the interpreter
    tracker._set_slot("requested_language", "en")
    inte=RasaNLUHttpInterpreter(EndpointConfig(url))
    result = await inte.parse(message, tracker=tracker)
    return result

class MultiNluClient(object):
    async def raw_invoke(self):
        result=await nlu_parse(DEFAULT_SERVER_URL, 'hi')
        pprint(result)

    async def simulate(self):
        result = await nlu_parse('http://localhost:5009/simulate/en', 'hi')
        pprint(result)

    async def multilang(self, lang, text):
        result = await nlu_parse(f'http://localhost:5009/nlu/{lang}', text)
        return result

multi_nlu=MultiNluClient()


