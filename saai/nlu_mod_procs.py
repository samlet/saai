import json
import json_utils

prefix = '/pi/ws/sagas-ai/nlu_multilang'
def train_mod(lang):
    from rasa.train import train_nlu, train_async
    from saai.tools.corpus_procs import CorpusProcs
    if lang in ('ja','zh'):
        # saai.tools.corpus_procs gen_datasets cn '/pi/ws/sagas-ai/nlu_multilang/zh/'
        CorpusProcs().gen_datasets('cn' if lang=='zh' else lang, f'{prefix}/{lang}/')
    train_nlu(
        config=f"{prefix}/config_{lang}.yml",
        nlu_data=f"{prefix}/{lang}/",
        output=f'{prefix}/models',
        fixed_model_name='{lang}_current',
        persist_nlu_training_data=True
    )

def load_mod(lang):
    from rasa.core.agent import Agent, load_agent
    # from rasa.nlu.model import Interpreter
    path = f'{prefix}/models/{lang}_current.tar.gz'
    # interpreter = Interpreter.load(path)
    agent = Agent.load(path)
    return agent

async def intepret(agent, text):
    interpreter = agent.interpreter
    return await interpreter.parse(text)

class NluModProcs(object):
    mods = ('de', 'en', 'es', 'fr', 'ru', 'corpus')

    def __init__(self):
        self.timestamps_file=f'{prefix}/last_timestamps.json'

    def get_timestamps(self):
        import io_utils
        import os

        last_timestamps = {}
        for mod in self.mods:
            folder = f"{prefix}/{mod}/"
            # print(folder)
            # print(os.listdir(folder))
            files = [(f, os.path.getmtime(f)) for f in io_utils.list_files(folder)
                     if os.path.isfile(f)]
            # print(len(files))
            files = sorted(files, key=lambda x: x[1], reverse=True)
            last_modified_file = None if len(files) == 0 else files[0][0]
            if last_modified_file is not None:
                mark = os.path.getmtime(last_modified_file)
                # print(last_modified_file, mark)
                last_timestamps[mod] = mark
        return last_timestamps

    def write_timestamps(self):
        """
        $ python -m saai.nlu_mod_procs write_timestamps
        :return:
        """
        last_timestamps = self.get_timestamps()
        print(last_timestamps)
        json_utils.write_json_to_file(self.timestamps_file, last_timestamps)

    def check_modified(self):
        """
        $ python -m saai.nlu_mod_procs check_modified
        :return:
        """
        before = json_utils.read_json_file(self.timestamps_file)
        current = self.get_timestamps()
        modified = []
        for item in current:
            if current[item] - before[item] > 1:
                modified.append(item)
        return modified

    def train(self, lang):
        """
        $ python -m saai.nlu_mod_procs train zh
        :param lang:
        :return:
        """
        train_mod(lang)

    def parse(self, sents, lang):
        """
        $ python -m saai.nlu_mod_procs parse 'hi' en

        :param sents:
        :param lang:
        :return:
        """
        import asyncio

        agent=load_mod(lang)
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(intepret(agent, sents))

    def parse_pp(self, sents, lang):
        """
        $ python -m saai.nlu_mod_procs parse_pp 'hi' en
        """
        from pprint import pprint
        pprint(self.parse(sents, lang))


if __name__ == '__main__':
    import fire
    fire.Fire(NluModProcs)

