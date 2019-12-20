from saai.multilang_tokenizer import MultilangTokenizer

from rasa.nlu.training_data import TrainingData, Message
from rasa.nlu.tokenizers.whitespace_tokenizer import WhitespaceTokenizer
import requests
import asyncio

def testing_tokenizer(text, cls, lang='en'):
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
    def comps(self):
        """
        $ python -m saai.saai_cli comps
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

    def bot_reload(self, bot='genesis'):
        """
        $ python -m saai.saai_cli bot_reload genesis
        :param bot:
        :return:
        """
        response = requests.post(f'http://localhost:18099/reload', json={'mod': bot})
        print('status code:', response.status_code)
        return response.json()

    def multilang_nlu(self, lang, text):
        """
        $ python -m saai.saai_cli multilang_nlu en 'hi'

        :param lang:
        :param text:
        :return:
        """
        from saai.multi_nlu_client import multi_nlu

        loop = asyncio.get_event_loop()
        return loop.run_until_complete(multi_nlu.multilang(lang, text))

if __name__ == '__main__':
    import fire
    from sagas.tool.loggers import init_logger

    init_logger()
    fire.Fire(SaaiCli)
