import json
import json_utils
import sagas.tracker_fn as tc

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
        fixed_model_name=f'{lang}_current',
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

mods = ('de', 'en', 'es', 'fr', 'ru', 'corpus')
langs = {'de', 'en', 'fr', 'ru', 'es', 'zh', 'ja'}
class NluMods(object):
    def __init__(self):
        self.mods = {}

    async def parse_async(self, sents, lang):
        if lang not in langs:
            return {}
        if lang not in self.mods:
            self.mods[lang]=load_mod(lang)
        return await intepret(self.mods[lang], sents)

    def reload(self, lang):
        # train_mod(lang)
        self.mods[lang] = load_mod(lang)
        # return await intepret(self.mods[lang], 'hi')
        return True

class NluModProcs(object):
    def __init__(self):
        self.timestamps_file=f'{prefix}/last_timestamps.json'

    def get_timestamps(self):
        import io_utils
        import os

        last_timestamps = {}
        for mod in mods:
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
        import os

        if not os.path.exists(self.timestamps_file):
            return mods

        before = json_utils.read_json_file(self.timestamps_file)
        current = self.get_timestamps()
        modified = []
        for item in current:
            if current[item] - before[item] > 1:
                modified.append(item)
        return modified

    def train_all(self, force=False):
        """
        $ python -m saai.nlu_mod_procs train_all
        :return:
        """
        if force:
            train_set=mods
        else:
            train_set=self.check_modified()
        if len(train_set)>0:
            for lang in train_set:
                if lang=='corpus':
                    tc.emp('green', 'train zh,ja ...')
                    train_mod('zh')
                    train_mod('ja')
                else:
                    tc.emp('green', f'train {lang} ...')
                    train_mod(lang)
            self.write_timestamps()
        else:
            tc.emp('yellow', 'all up-to-date.')

    def train(self, lang):
        """
        $ python -m saai.nlu_mod_procs train zh
        $ python -m saai.nlu_mod_procs train en
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
        $ python -m saai.nlu_mod_procs parse_pp '附近有什么好吃的' zh
        """
        from pprint import pprint
        pprint(self.parse(sents, lang))

nlu_mods=NluMods()

if __name__ == '__main__':
    import fire
    from sagas.tool.loggers import init_logger

    init_logger()
    fire.Fire(NluModProcs)

