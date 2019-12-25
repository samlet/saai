from typing import Any, Dict, List, Text

from rasa.nlu.extractors import EntityExtractor
from rasa.nlu.training_data import Message
from sagas.conf.conf import cf

class FacadeEntityExtractor(EntityExtractor):

    provides = ["entities"]
    defaults = {
        # by default all dimensions recognized
        # dimensions can be configured to contain an array of strings
        # with the names of the dimensions to filter for
        "dimensions": None,
        "route": 'spacy/en',
    }

    def __init__(self, component_config: Text = None) -> None:
        super().__init__(component_config)

    def process(self, message: Message, **kwargs: Any) -> None:
        # print('..... ner_facade .......')
        all_extracted = self.add_extractor_name(self.extract_entities(message.text))
        dimensions = self.component_config["dimensions"]
        extracted = FacadeEntityExtractor.filter_irrelevant_entities(
            all_extracted, dimensions
        )
        message.set(
            "entities", message.get("entities", []) + extracted,
            add_to_output=True
        )

    def extract_entities(self, text: Text) -> List[Dict[Text, Any]]:
        import requests
        data = {"sents": text}
        route=self.component_config["route"]
        response = requests.post(f'{cf.ensure("facade")}/ner/{route}', json=data)
        if response.status_code==200:
            ents=response.json()
            entities = [
                {
                    "entity": ent['entity'],
                    "value": ent['text'],
                    "start": ent['start'],
                    "confidence": None,
                    "end": ent['end'],
                }
                for ent in ents
            ]
            return entities
        else:
            print(f".. error code {response.status_code}")
            return []

