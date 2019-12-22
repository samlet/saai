from typing import Any, Dict, List, Text
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.nlu.constants import (
    # MESSAGE_RESPONSE_ATTRIBUTE,
    # MESSAGE_INTENT_ATTRIBUTE,
    # MESSAGE_TEXT_ATTRIBUTE,
    # MESSAGE_TOKENS_NAMES,
    TEXT_ATTRIBUTE,
    MESSAGE_ATTRIBUTES,
    # MESSAGE_SPACY_FEATURES_NAMES,
    # MESSAGE_VECTOR_FEATURE_NAMES,
)

from sagas.util.rest_common import query_data_by_url
from rasa.nlu.training_data import TrainingData, Message
from rasa.nlu.tokenizers.whitespace_tokenizer import WhitespaceTokenizer
from sagas.conf.conf import cf

class MultilangTokenizer(WhitespaceTokenizer):
    def __init__(self, component_config: Dict[Text, Any] = None) -> None:
        """Construct a new tokenizer using the WhitespaceTokenizer framework."""
        super().__init__(component_config)
        self.lang = self.component_config["lang"]
        print(f".. tokenizer with lang {self.lang}")

    def tokenize(
            self, text: Text, attribute: Text = TEXT_ATTRIBUTE
    ) -> List[Token]:
        if self.lang in ('zh', 'ja'):
            r = query_data_by_url(cf.servant_by_lang(self.lang), 'tokens', {'lang': self.lang, 'sents': text})
            words = r['data']
            running_offset = 0
            tokens = []
            for word in words:
                word_offset = text.index(word, running_offset)
                word_len = len(word)
                running_offset = word_offset + word_len
                tokens.append(Token(word, word_offset))
            return tokens
        return super().tokenize(text, attribute)


