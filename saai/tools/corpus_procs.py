import json
import json_utils
import io

class EntityData(object):
    def __init__(self, start, end, value, entity):
        self.start=start
        self.end=end
        self.value=value
        self.entity=entity
        
    @property
    def json(self):
        return {
            "start":self.start,
            "end":self.end,
            "value":self.value,
            "entity":self.entity
        }
    
class FactData(object):
    def __init__(self, text, intent):
        self.text=text
        self.intent=intent
        self.entities=[]
        
    @property
    def json(self):
        return {
            "text":self.text,
            "intent":self.intent,
            "entities":[u.json for u in self.entities]
        }
    
class NluData(object):
    def __init__(self):
        self.examples=[]
        
    @property
    def json(self):
        return {
          "rasa_nlu_data": {
            "common_examples": [u.json for u in self.examples]
          }
        }

def parse(dataset, intent, sentence):
    from saai.dataset.intent_dataset import IntentUtterance, SlotChunk
    # from snips_nlu.dataset.intent import IntentUtterance, SlotChunk
    u = IntentUtterance.parse(sentence)
    fact=FactData(u.input, intent)
    # fact = FactData(u.text, intent)
    for chunk in u.chunks:    
        if type(chunk)==SlotChunk:
            print("\t{}: {}-{}".format(chunk.text,
                chunk.range.start,
                chunk.range.end))
            entity=EntityData(chunk.range.start, chunk.range.end, chunk.text, chunk.name)
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
                    entity=EntityData(c["start"], c["end"], c["value"], c["entity"])
                    fact.entities.append(entity)
            dataset.examples.append(fact)
        print(json.dumps(dataset.json, indent=2, sort_keys=False, ensure_ascii=False))

    ## ./corpus_procs.py gen_dataset corpus/cn-Samples.md json/cn-Samples.json
    def gen_dataset(self, filename, output):
        f = open(filename)
        lines=f.readlines()
        f.close()

        dataset=NluData()
        intent=""
        for line in lines:
            line_s=line.strip()
            if line.startswith("##"):        
                intent=line[3:].strip()
                print("☈", intent)
            elif len(line_s)==0 or line_s.startswith("#"):
                pass
            else:
                parse(dataset, intent, line_s)


        result=(json.dumps(dataset.json, indent=2, sort_keys=False, ensure_ascii=False))
        with io.open(output, 'w', encoding="utf-8") as f:
            f.write(result)

        print(f".. write to {output} ok.")

    def gen_datasets(self, lang_prefix='cn', target_prefix='zh/'):
        import glob
        import os
        prefix='.'
        trans_files = [(x, target_prefix + os.path.basename(x).replace('.md', '.json')) for x in
                       glob.glob(f'{prefix}/corpus/{lang_prefix}-*.md')]
        for f in trans_files:
            self.gen_dataset(f[0], f[1])

if __name__ == '__main__':
    import fire
    fire.Fire(CorpusProcs)

