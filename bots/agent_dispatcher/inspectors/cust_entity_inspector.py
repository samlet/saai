from typing import Text, Any, Dict, List
from sagas.nlu.inspector_common import Inspector, Context
import logging
logger = logging.getLogger(__name__)

def get_entities(sents:Text):
    from saai.tool import rasa_nlu_parse
    result = rasa_nlu_parse(sents, 'http://localhost:15008')
    ents = result['entities']
    return ents

def get_entity_mapping(sents, doc, ents):
    running_offset = 0
    rs = []
    for token in doc.words:
        word = token.text
        word_offset = sents.find(word, running_offset)
        if word_offset>-1:
            word_len = len(word)
            running_offset = word_offset + word_len
            logger.debug(f"{word} - ({word_offset}, {running_offset})")
            for ent in ents:
                start, end=ent['start'], ent['end']
                if word_offset>=start and running_offset<=end:
                    rs.append({"start": word_offset,
                               "end": running_offset,
                               'index': token.index,
                               'value': word,
                               'entity': ent['entity']
                               })
    return rs

def get_children_index(sent, word_idx):
    from sagas.nlu.corenlp_parser import get_children
    rs = []
    word=next(filter(lambda w: w.index == word_idx, sent.words))
    get_children(sent, word, rs, stem=False)
    return [word_idx]+[w[0] for w in rs]


class CustEntityInspector(Inspector):
    def __init__(self, test_ent):
        # self.arg = arg
        self.test_ent=test_ent

    def name(self):
        return "cust_ents"

    def run(self, key, ctx: Context):
        from sagas.nlu.ruleset_procs import list_words, cached_chunks, get_main_domains
        from sagas.conf.conf import cf

        logger.debug(f".. check against {key}")
        if key not in ctx.indexes:
            return False

        # lemma = ctx.lemmas[key]
        sents = ctx.sents
        lang = ctx.lang
        chunks = cached_chunks(sents, lang, cf.engine(lang))
        doc=chunks['doc']
        ents=get_entities(sents)

        prt=ctx.indexes[key]
        indexes = get_children_index(doc, prt)
        idx_ent = {el['index']: el['entity'] for el in get_entity_mapping(sents, doc, ents)}
        children_ents = [(idx, idx_ent[idx] if idx in idx_ent else '_') for idx in indexes]

        result= self.test_ent in {e[1] for e in children_ents}
        if result:
            ctx.add_result(self.name(), 'default', key, idx_ent)
        return result

    def __str__(self):
        return f"ins_{self.name()}({self.test_ent})"

