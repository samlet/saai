#!/usr/bin/env python
# coding: utf8

"""Example of defining and (pre)training spaCy's knowledge base,
which is needed to implement entity linking functionality.

For more details, see the documentation:
* Knowledge base: https://spacy.io/api/kb
* Entity Linking: https://spacy.io/usage/linguistic-features#entity-linking

Compatible with: spaCy v2.2.3
Last tested with: v2.2.3
"""
from __future__ import unicode_literals, print_function

import plac
from pathlib import Path

from spacy.vocab import Vocab
import spacy
from spacy.kb import KnowledgeBase

from train_descriptions import EntityEncoder


# Q2146908 (Russ Cochran): American golfer
# Q7381115 (Russ Cochran): publisher
ENTITIES = {"Q2146908": ("American golfer", 342), "Q7381115": ("publisher", 17)}

INPUT_DIM = 300  # dimension of pretrained input vectors
DESC_WIDTH = 64  # dimension of output entity vectors


@plac.annotations(
    model=("Model name, should have pretrained word embeddings", "positional", None, str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int),
)
def main(model=None, output_dir=None, n_iter=50):
    """Load the model, create the KB and pretrain the entity encodings.
    If an output_dir is provided, the KB will be stored there in a file 'kb'.
    The updated vocab will also be written to a directory in the output_dir."""

    nlp = spacy.load(model)  # load existing spaCy model
    print("Loaded model '%s'" % model)

    # check the length of the nlp vectors
    if "vectors" not in nlp.meta or not nlp.vocab.vectors.size:
        raise ValueError(
            "The `nlp` object should have access to pretrained word vectors, "
            " cf. https://spacy.io/usage/models#languages."
        )

    kb = KnowledgeBase(vocab=nlp.vocab)

    # set up the data
    entity_ids = []
    descriptions = []
    freqs = []
    for key, value in ENTITIES.items():
        desc, freq = value
        entity_ids.append(key)
        descriptions.append(desc)
        freqs.append(freq)

    # training entity description encodings
    # this part can easily be replaced with a custom entity encoder
    encoder = EntityEncoder(
        nlp=nlp,
        input_dim=INPUT_DIM,
        desc_width=DESC_WIDTH,
        epochs=n_iter,
    )
    encoder.train(description_list=descriptions, to_print=True)

    # get the pretrained entity vectors
    embeddings = encoder.apply_encoder(descriptions)

    # set the entities, can also be done by calling `kb.add_entity` for each entity
    kb.set_entities(entity_list=entity_ids, freq_list=freqs, vector_list=embeddings)

    # adding aliases, the entities need to be defined in the KB beforehand
    kb.add_alias(
        alias="Russ Cochran",
        entities=["Q2146908", "Q7381115"],
        probabilities=[0.24, 0.7],  # the sum of these probabilities should not exceed 1
    )

    # test the trained model
    print()
    _print_kb(kb)

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        kb_path = str(output_dir / "kb")
        kb.dump(kb_path)
        print()
        print("Saved KB to", kb_path)

        vocab_path = output_dir / "vocab"
        kb.vocab.to_disk(vocab_path)
        print("Saved vocab to", vocab_path)

        print()

        # test the saved model
        # always reload a knowledge base with the same vocab instance!
        print("Loading vocab from", vocab_path)
        print("Loading KB from", kb_path)
        vocab2 = Vocab().from_disk(vocab_path)
        kb2 = KnowledgeBase(vocab=vocab2)
        kb2.load_bulk(kb_path)
        _print_kb(kb2)
        print()


def _print_kb(kb):
    print(kb.get_size_entities(), "kb entities:", kb.get_entity_strings())
    print(kb.get_size_aliases(), "kb aliases:", kb.get_alias_strings())


if __name__ == "__main__":
    plac.call(main)

    # Expected output:

    # 2 kb entities: ['Q2146908', 'Q7381115']
    # 1 kb aliases: ['Russ Cochran']
