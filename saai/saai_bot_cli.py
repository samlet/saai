from typing import Text

import requests
from pprint import pprint

def ask_overwrite(path: Text) -> None:
    import questionary
    import os

    overwrite = questionary.confirm(
        "Directory '{}' is not empty. Continue?".format(os.path.abspath(path))
    ).ask()
    return overwrite

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

    def talk(self, sents, sender='default', port=5005):
        """
        $ saai talk 'hello' samlet 15008

        :param sender:
        :return:
        """
        response = requests.post(f'http://localhost:{port}/webhooks/rest/webhook',
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

    def scaffold_info(self):
        """
        $ saai scaffold_info
        :return:
        """
        from saai.scaffold.project_creator import scaffold_path
        print(f"{scaffold_path()}")

    def init_proj(self, proto='en', train_it=False):
        """
        $ saai init_proj zh True
        :param proto:
        :param train_it:
        :return:
        """
        from saai.scaffold.project_creator import create_initial_project, train_project

        import os
        path=os.path.abspath('.')
        if len(os.listdir(path)) > 0:
            if not ask_overwrite(path):
                return

        create_initial_project(path, proto=proto)
        if train_it:
            if len(os.listdir("./corpus")):
                self.gen_corpus()
            train_project(path)

    def build(self, file:Text):
        """
        $ saai build servant-stack.dockerfile
        :param file:
        :return:
        """
        import subprocess
        if file.endswith('.dockerfile'):
            image_name=file.replace('.dockerfile', '').replace('-', '_')
            subprocess.run(["docker", "build",
                            '-t', f"samlet/{image_name}",
                            '-f', file, '.'])
        else:
            print(".. don't support this file type.")
