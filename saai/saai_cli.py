import requests
import asyncio
from pprint import pprint

def testing_tokenizer(text, cls, lang='en'):
    from rasa.nlu.training_data import TrainingData, Message
    defaults = {
        # Flag to check whether to split intents
        "intent_tokenization_flag": False,
        # Symbol on which intent should be split
        "intent_split_symbol": "_",
        # text will be tokenized with case sensitive as default
        "case_sensitive": True,
        "lang": lang,
    }

    tok=cls(defaults)
    example = Message(text, {
            "intent": "wish",
            "entities": []})
    # tokenizer
    tok.process(example, x='.')
    for token in example.get("tokens"):
        print(token.text, token.offset)

class SaaiCli(object):
    def version(self):
        from saai.version import __version__
        print(f"saai version: {__version__}")

    def comps(self):
        """
        $ python -m saai.saai_cli comps
        $ python -m saai comps

        :return:
        """
        from rasa.nlu import config
        conf = config.load('saai/sample_configs/config_tokenizer.yml')
        # conf.for_component('DucklingHTTPExtractor')
        return conf.component_names

    def tokens(self, text, lang):
        """
        $ python -m saai.saai_cli tokens "在终端上输出单词的定义和继承链" zh
        :param text:
        :param lang:
        :return:
        """
        from saai.multilang_tokenizer import MultilangTokenizer
        print(testing_tokenizer(text, MultilangTokenizer, lang))

    def bot_message(self, lang='en'):
        """
        $ python -m saai.saai_cli bot_message
        :param lang:
        :return:
        """
        # sents = '/behave_purpose{"object_type": "restaurant"}'
        # data = {'mod': 'genesis', 'lang': lang, "sents": sents}
        text = '/behave_purpose{"object_type": "text", "sents":"%s"}' % "do you have any restaurants"
        data = {'mod': 'genesis', 'lang': lang, "sents": text}
        response = requests.post(f'http://localhost:18099/message/my', json=data)
        print('status code:', response.status_code)
        return response.json()

    def nlu_ner(self, route, sents):
        """
        $ python -m saai.saai_cli nlu_ner spacy/en "I was born in Beijing."
        $ python -m saai.saai_cli nlu_ner id "Jokowi pergi ke Singapura."
        :param route:
        :param sents:
        :return:
        """
        data={"sents":sents}
        response = requests.post(f'http://localhost:1700/ner/{route}', json=data)
        print('status code:', response.status_code)
        pprint(response.json())

    def bot_reload(self, bot='genesis'):
        """
        $ python -m saai.saai_cli bot_reload genesis
        :param bot:
        :return:
        """
        response = requests.post(f'http://localhost:18099/reload', json={'mod': bot})
        print('status code:', response.status_code)
        return response.json()

    def nlu_parse(self, sents, lang='en'):
        """ Nlu parse routines
        $ python -m saai.saai_cli nlu_parse "Shenzhen ist das Silicon Valley für Hardware-Firmen" de
        $ python -m saai.saai_cli nlu_parse '附近有什么好吃的' zh
        $ python -m saai.saai_cli nlu_parse '六安市公安局裕安分局平桥派出所接到辖区居民戴某报警' zh
        $ python -m saai.saai_cli nlu_parse '一直打喷嚏怎么办' zh
        $ python -m saai.saai_cli nlu_parse "I was born in Beijing." en
        $ python -m saai.saai_cli nlu_parse "Я хочу поехать в москву" ru
        $ python -m saai.saai_cli nlu_parse "Jokowi pergi ke Singapura." id

        :param sents:
        :param lang:
        :return:
        """
        from sagas.conf.conf import cf
        from sagas.nlu.rasa_procs import invoke_nlu
        import json
        import sagas.tracker_fn as tc

        endpoint = cf.ensure('nlu_multilang_servant')
        print('.. with endpoing', endpoint)
        result = invoke_nlu(endpoint, lang, "current", sents)
        tc.emp('yellow', result)
        if result != None and len(result)>0:
            print(json.dumps(result, indent=4, ensure_ascii=False))

            intent = result["intent"]
            print('%s -> %f' % (intent['name'], intent['confidence']))
            entities = result['entities']
            print('entities ->', [ent['entity'] for ent in entities])

    def nlu_reload(self, lang='en'):
        """
        $ python -m saai.saai_cli nlu_reload en
        # or train and reload in docker env
        $ docker exec -it sagas_agent_servant_1 python -m saai.saai_cli nlu_reload en

        :param bot:
        :return:
        """
        from saai.nlu_mod_procs import train_mod
        print('.. training')
        train_mod(lang)
        print('.. reloading')
        response = requests.post(f'http://localhost:18099/reload_nlu', json={'mod': lang})
        print('status code:', response.status_code)
        return response.json()

    def multilang_nlu(self, lang, text):
        """
        $ python -m saai.saai_cli multilang_nlu en 'hi'
        $ python -m saai.saai_cli multilang_nlu en "I was born in Beijing."
        $ python -m saai.saai_cli multilang_nlu en "I was born in the spring of 1982."
        $ python -m saai.saai_cli multilang_nlu en "tomorrow at eight"
        $ python -m saai.saai_cli multilang_nlu ja "太郎は5月18日の朝9時に花子に会いに行った"
        $ python -m saai.saai_cli multilang_nlu ja "お皿を二枚ください。"

        :param lang:
        :param text:
        :return:
        """
        from saai.multi_nlu_client import multi_nlu
        from pprint import pprint

        loop = asyncio.get_event_loop()
        r= loop.run_until_complete(multi_nlu.multilang(lang, text))
        pprint(r)

if __name__ == '__main__':
    import fire
    from sagas.tool.loggers import init_logger

    init_logger()
    fire.Fire(SaaiCli)
