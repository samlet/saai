from durable.lang import *
from durable.engine import Host

with ruleset('verbs'):
    @when_all(m.lemma.matches('want.*'))
    def verb_want(c):
        # c.s.matches = True
        print('1. verb matches pat -> {0}'.format(c.m.text))


    @when_all(m.xpos.matches('VBP.*'))
    def verb_xpos(c):
        c.s.pos_matches = True
        print('2. verb xpos matches pat -> {0}'.format(c.m.xpos))


    @when_all(m.domains.amod.specs.anyItem(item.matches('.*thing.*, entity.*')))
    def amod_with(c):
        c.s.amod_with = True
        print('3. amod pat -> {0}'.format(c.domains.amod))


    @when_all(m.xcomp.anyItem(item.text.matches('play')))
    def xcomp_play(c):
        # print ('xcomp pat -> {0}'.format(c.m.domains.xcomp.text))
        print('4. xcomp pat')


    @when_all(m.nsubj.anyItem(item.text.matches('I')))
    def subj_play(c):
        # print ('xcomp pat -> {0}'.format(c.m.domains.xcomp.text))
        print('5. nsubj pat')

with ruleset('risk'):
    @when_all(c.first << m.t == 'purchase',
              c.second << m.location != c.first.location)
    # the event pair will only be observed once
    def fraud(c):
        print('risk-> Fraud detected -> {0}, {1}'.format(c.first.location, c.second.location))


class RulesTests(object):
    def tests_1(self):
        """
        $ python -m saai.tests.rules_tests tests_1
        :return:
        """
        v = {'nsubj': [{'index': '1', 'text': 'I'}],
             'xcomp': [{'index': '4',
                       'text': 'play',
                       'lemma': 'play',
                       'upos': 'VERB',
                       'xpos': 'VB',
                       'feats': 'VerbForm=Inf',
                       'governor': 2,
                       'dependency_relation': 'xcomp',
                       'mark': [{'index': '3',
                                'text': 'to',
                                'lemma': 'to',
                                'upos': 'PART',
                                'xpos': 'TO',
                                'feats': '_',
                                'governor': 4,
                                'dependency_relation': 'mark'}],
                       'obj': [{'index': '5',
                               'text': 'music',
                               'lemma': 'music',
                               'upos': 'NOUN',
                               'xpos': 'NN',
                               'feats': 'Number=Sing',
                               'governor': 4,
                               'dependency_relation': 'obj'}]}],
             "index": "2",
             "text": "want", "lemma": "want",
             "upos": "VERB",
             "xpos": "VBP",
             "feats": "Mood=Ind|Tense=Pres|VerbForm=Fin",
             "governor": 0, "dependency_relation": "root"}
        print(assert_fact('verbs', v))

    def tests_2(self):
        """
        $ python -m saai.tests.rules_tests tests_2
        :return:
        """
        # 'post' submits events, try 'assert' instead and to see differt behavior
        # post('risk', {'t': 'purchase', 'location': 'US'})
        # post('risk', {'t': 'purchase', 'location': 'CA'})
        post_batch('risk', [{'t': 'purchase', 'location': 'US'},{'t': 'purchase', 'location': 'CA'}])
        print('..')
        assert_fact('risk', {'t': 'purchase', 'location': 'US'})
        assert_fact('risk', {'t': 'purchase', 'location': 'CA'})

if __name__ == '__main__':
    import fire
    fire.Fire(RulesTests)

