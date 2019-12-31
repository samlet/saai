import requests
from pprint import pprint

class SaaiBotCli(object):
    def version(self):
        """
        Show saai version info
        :return:
        """
        from saai.version import __version__
        print(f"saai version: {__version__}")

    def gen_corpus(self):
        """
        Generate corpus data
        :return:
        """
        from saai.tools.corpus_procs import CorpusProcs
        proc=CorpusProcs()
        proc.gen_local()

    def train(self):
        """
        Generate and train nlu data
        :return:
        """
        import subprocess

        self.gen_corpus()
        subprocess.run(["rasa", "train"])

    def parse(self, sents):
        """
        $ saai parse '感觉发烧了，该去哪个诊所哪个科室呢'

        :param sents:
        :return:
        """
        response = requests.post(f'http://localhost:5005/model/parse', json={'text': sents})
        print('status code:', response.status_code)
        pprint(response.json())

    def talk(self, sents, sender='default'):
        """
        $ saai talk 'hello'

        :param sender:
        :return:
        """
        response = requests.post(f'http://localhost:5005/webhooks/rest/webhook',
                                 json={'message': sents, 'sender':sender})
        print('status code:', response.status_code)
        pprint(response.json())

    def reset_conversation(self, sender='default'):
        """
        $ saai reset_conversation

        :param sender:
        :return:
        """
        response = requests.post(f'http://localhost:5005/conversations/{sender}/tracker/events',
                                 json={'event': 'restart'})
        print('status code:', response.status_code)
