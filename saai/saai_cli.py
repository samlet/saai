from saai.multilang_tokenizer import MultilangTokenizer

from rasa.nlu.training_data import TrainingData, Message
from rasa.nlu.tokenizers.whitespace_tokenizer import WhitespaceTokenizer

def testing_tokenizer(text, cls, lang='en'):
    defaults = {
        # Flag to check whether to split intents
        "intent_tokenization_flag": False,
        # Symbol on which intent should be split
        "intent_split_symbol": "_",
        # text will be tokenized with case sensitive as default
        "case_sensitive": True,
        "lang": lang,
    }

    tok=cls(defaults)
    example = Message(text, {
            "intent": "wish",
            "entities": []})
    # tokenizer
    tok.process(example, x='.')
    for token in example.get("tokens"):
        print(token.text, token.offset)

class SaaiCli(object):
    def tokens(self, text, lang):
        """
        $ python -m saai.saai_cli tokens "在终端上输出单词的定义和继承链" zh
        :param text:
        :param lang:
        :return:
        """
        print(testing_tokenizer(text, MultilangTokenizer, lang))

if __name__ == '__main__':
    import fire
    fire.Fire(SaaiCli)
