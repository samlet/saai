from typing import Any, Dict, List, Text
from rasa.nlu.tokenizers.tokenizer import Token

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

    # def tokenize(
    #         self, text: Text, attribute: Text = TEXT_ATTRIBUTE
    # ) -> List[Token]:
    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        text = message.get(attribute)
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
        return super().tokenize(message, attribute)


