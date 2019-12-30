from typing import Any, Dict, List, Text

from rasa.nlu.extractors import EntityExtractor
from rasa.nlu.training_data import Message

def extract_entities(sents):
    import jieba.posseg as pseg
    words = pseg.cut(sents,use_paddle=True)
    tokens=[(word, flag) for word, flag in words]
    running_offset = 0
    rs = []
    for token in tokens:
        word = token[0]
        word_offset = sents.index(word, running_offset)
        word_len = len(word)
        running_offset = word_offset + word_len
        rs.append({"start": word_offset,
                   "end": running_offset,
                   'value': word,
                   'entity': token[1],
                   "confidence": None,
                   })
    return [w for w in rs if w['entity'] in {'PER', 'LOC', 'ORG', 'TIME'}]

class JiebaEntityExtractor(EntityExtractor):

    provides = ["entities"]
    defaults = {
        # by default all dimensions recognized
        # dimensions can be configured to contain an array of strings
        # with the names of the dimensions to filter for
        "dimensions": None
    }

    def __init__(self, component_config: Text = None) -> None:
        super().__init__(component_config)

    def process(self, message: Message, **kwargs: Any) -> None:
        all_extracted = self.add_extractor_name(extract_entities(message.text))
        dimensions = self.component_config["dimensions"]
        extracted = JiebaEntityExtractor.filter_irrelevant_entities(
            all_extracted, dimensions
        )
        message.set(
            "entities", message.get("entities", []) + extracted,
            add_to_output=True
        )


