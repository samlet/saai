import requests

from honcho.manager import Manager
import sys
import logging
logger = logging.getLogger(__name__)

def invoke_nlu(url, text):
    headers = {
        'content-type': 'application/json',
    }
    params = {
        "text": text
    }
    try:
        result = requests.post(url, headers=headers, json=params)
        if result.status_code == 200:
            return result.json()
        else:
            logger.error(
                "Failed to parse text '{}' using rasa NLU over http. "
                "Error: {}".format(text, result.text))
            return None
    except Exception as e:
        logger.error(
            "Failed to parse text '{}' using rasa NLU over http. "
            "Error: {}".format(text, e))
        return None


class Runner(object):
    def __init__(self, start_port=2000):
        self.nlu_servants={}
        for i, lang in enumerate(['en','zh','ja','es','fr','de','ru']):
            self.nlu_servants[lang]=start_port+i

    def tests(self):
        """
        $ python -m saai.runner tests
        :return:
        """
        m = Manager()
        m.add_process('nlu_en', './startup.run nlu en 2001')
        m.add_process('nlu_zh', './startup.run nlu zh 2002')
        m.loop()

        sys.exit(m.returncode)

    def exec_spec(self, langs):
        """
        $ python -m saai.runner exec_spec zh,en,ja
        $ python -m saai.runner exec_spec zh,en,ja,de
        :param langs:
        :return:
        """
        m = Manager()
        for lang in langs:
            port=self.nlu_servants[lang]
            m.add_process(f'nlu_{lang}', f'./startup.run nlu {lang} {port}')
        m.loop()

        sys.exit(m.returncode)

    def invoke(self, sents, lang, port=0):
        """
        $ python -m saai.runner invoke "几台电脑" zh
        $ python -m saai.runner invoke "卵を食べる" ja
        $ python -m saai.runner invoke "can i get french food" en
        $ python -m saai.runner invoke "Shenzhen ist das Silicon Valley für Hardware-Firmen" de

        :param sents:
        :param lang:
        :return:
        """
        from pprint import pprint

        if port ==0:
            port = self.nlu_servants[lang]
        url=f"http://localhost:{port}/model/parse"
        r=invoke_nlu(url, sents)
        if r is not None:
            pprint(r)
            print('done.')

if __name__ == '__main__':
    import fire
    from sagas.tool.loggers import init_logger

    init_logger()
    fire.Fire(Runner)

