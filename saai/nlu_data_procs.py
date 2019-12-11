from rasa.importers.utils import training_data_from_paths

class NluDataProcs(object):
    def view_file(self, file, lang='en'):
        """
        $ python -m saai.nlu_data_procs view_file ./nlu_multilang/en/nlu_data.md
        $ python -m saai.nlu_data_procs view_file /pi/ws/knowledgebasebot/data/nlu.md

        :param file:
        :param lang:
        :return:
        """
        from pprint import pprint
        # files = ['./nlu_multilang/en/nlu_data.md']
        td = training_data_from_paths([file], language=lang)
        print('.. intents')
        print(td.intents)
        print('.. entities')
        print(td.entities)
        print('.. examples')
        # print(*[e.text for e in td.training_examples], sep='\n')
        print(*[(e.get("intent"), e.text) for e in td.training_examples], sep='\n')
        print('.. lookup_tables')
        pprint(td.lookup_tables)

    def train(self):
        from rasa.train import train_nlu
        prefix = '/pi/ws/sagas-ai/nlu_multilang'
        train_nlu(
            config=f"{prefix}/config_en.yml",
            nlu_data=f"{prefix}/en/",
            output=f'{prefix}/models',
            fixed_model_name='en_current',
            persist_nlu_training_data=True
        )



if __name__ == '__main__':
    import fire
    fire.Fire(NluDataProcs)

