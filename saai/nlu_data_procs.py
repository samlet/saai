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

if __name__ == '__main__':
    import fire
    fire.Fire(NluDataProcs)

