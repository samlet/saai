from typing import Text, Dict, Sequence, List
import json
import json_utils
import io
import logging

logger = logging.getLogger(__name__)

class EntityData(object):
    def __init__(self, start, end, value, entity, norm):
        self.start=start
        self.end=end
        self.value=value
        self.entity=entity
        self.norm=norm
        # print('..', self.norm)
        
    @property
    def json(self):
        return {
            "start":self.start,
            "end":self.end,
            "value":self.value if self.norm=='o' else self.norm,
            "entity":self.entity
        }
    
class FactData(object):
    def __init__(self, text, intent):
        self.text=text
        self.intent=intent
        self.entities=[]  # EntityData

    def collect_synonyms(self):
        return [(x.norm, x.value) for x in self.entities if x.norm!='o']
        
    @property
    def json(self):
        return {
            "text":self.text,
            "intent":self.intent,
            "entities":[u.json for u in self.entities]
        }
    
class NluData(object):
    def __init__(self):
        self.examples=[]  # FactData

    def group_synonyms(self):
        import itertools
        import operator
        all_norms=[]
        for l in self.examples:
            all_norms.extend(l.collect_synonyms())
        it = itertools.groupby(all_norms, operator.itemgetter(0))
        for key, subiter in it:
            yield {"value":key, "synonyms": [item[1] for item in subiter]}

    @property
    def json(self):
        return {
          "rasa_nlu_data": {
            "common_examples": [u.json for u in self.examples],
            'entity_synonyms': list(self.group_synonyms())
          }
        }

def parse(dataset:NluData, intent:Text, sentence:Text):
    from saai.dataset.intent_dataset import IntentUtterance, SlotChunk
    # from snips_nlu.dataset.intent import IntentUtterance, SlotChunk
    u = IntentUtterance.parse(sentence)
    fact=FactData(u.input, intent)
    # fact = FactData(u.text, intent)
    for chunk in u.chunks:    
        if type(chunk)==SlotChunk:
            logger.debug("{}: {}-{}".format(chunk.text,
                chunk.range.start,
                chunk.range.end))
            entity=EntityData(chunk.range.start, chunk.range.end,
                              chunk.text, chunk.name, chunk.entity)
            fact.entities.append(entity)
    dataset.examples.append(fact)

class CorpusProcs(object):
    ## ./corpus_procs.py view_json_data "json/demo-rasa_zh.json"
    def view_json_data(self, file_name):
        data=json_utils.read_json_file(file_name)
        index=1
        for item in data["rasa_nlu_data"]["common_examples"]:
            print("{}. {} ({})".format(index, item["text"], item["intent"]))
            children=item['entities']
            if len(children)>0:
                for c in children:
                    print("\t{}-{}: {}({})".format(c["start"], c["end"], c["value"], c["entity"]))
            index=index+1

    def check_json(self, input_file):
        data=json_utils.read_json_file(input_file)
        dataset=NluData()
        for item in data["rasa_nlu_data"]["common_examples"]:
            # print("{}. {} ({})".format(index, item["text"], item["intent"]))
            fact=FactData(item["text"], item["intent"])
            children=item['entities']
            if len(children)>0:
                for c in children:
                    # print("\t{}-{}: {}({})".format(c["start"], c["end"], c["value"], c["entity"]))
                    entity=EntityData(c["start"], c["end"], c["value"], c["entity"], c["value"])
                    fact.entities.append(entity)
            dataset.examples.append(fact)
        print(json.dumps(dataset.json, indent=2, sort_keys=False, ensure_ascii=False))

    ## ./corpus_procs.py gen_dataset corpus/cn-Samples.md json/cn-Samples.json
    def gen_dataset(self, filename, output):
        with open(filename) as f:
            lines=f.readlines()

        dataset=NluData()
        intent=""
        for line in lines:
            line_s=line.strip()
            if line.startswith("##"):        
                intent=line[3:].strip()
                logger.debug(intent)
            elif len(line_s)==0 or line_s.startswith("#"):
                pass
            else:
                parse(dataset, intent, line_s)


        result=(json.dumps(dataset.json, indent=2, sort_keys=False, ensure_ascii=False))
        with io.open(output, 'w', encoding="utf-8") as f:
            f.write(result)

        logger.info(f".. write to {output} ok.")

    def gen_datasets(self, lang_prefix='cn', target_prefix='/pi/ws/sagas-ai/nlu_multilang/zh/'):
        import glob
        import os
        prefix='/pi/ws/sagas-ai/nlu_multilang'
        trans_files = [(x, target_prefix + os.path.basename(x).replace('.md', '.json')) for x in
                       glob.glob(f'{prefix}/corpus/{lang_prefix}-*.md')]
        for f in trans_files:
            self.gen_dataset(f[0], f[1])

    def gen_local(self):
        import glob
        import os

        target_prefix='./data/'
        prefix='./corpus'
        trans_files = [(x, target_prefix + os.path.basename(x).replace('.md', '.json')) for x in
                       glob.glob(f'{prefix}/*.md')]
        for f in trans_files:
            print(f'.. generate {f[0]} -> {f[1]}')
            self.gen_dataset(f[0], f[1])

if __name__ == '__main__':
    import fire
    fire.Fire(CorpusProcs)

