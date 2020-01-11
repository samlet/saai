from typing import Dict, Text, Any

from .ner_jieba import extract_entities as ner_jieba
import requests
import logging

logger = logging.getLogger(__name__)

def ner_jieba_vis(text):
    from ipymarkup.palette import palette, BLUE, RED, GREEN
    from ipymarkup import show_box_markup
    spans = [(w['start'], w['end'], w['entity']) for w in ner_jieba(text)]
    show_box_markup(text, spans, palette=palette(PER=BLUE, ORG=RED, LOC=GREEN))

def rasa_nlu_parse(sents) -> Dict[Text, Any]:
    response = requests.post(f'http://localhost:5005/model/parse', json={'text': sents})
    if response.status_code!=200:
        logger.warning(f'status code is {response.status_code}, fail to parse {sents}')
        return {}
    return response.json()

def rasa_nlu_vis(sents):
    from ipymarkup import show_box_markup

    result = rasa_nlu_parse(sents)
    if len(result)>0:
        ents = result['entities']
        spans = [(w['start'], w['end'], w['entity']) for w in ents]
        show_box_markup(sents, spans)

