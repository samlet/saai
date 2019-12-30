import streamlit as st

from interacts.common import display_lang_selector
from interacts.sl_utils import all_labels, write_styles
from interacts.tracker_streamlit import enable_streamlit_tracker

from sagas.conf.conf import cf
from sagas.nlu.ruleset_procs import parse_sents, equals, group_by, children
from sagas.nlu.uni_remote_viz import list_contrast, display_doc_deps

enable_streamlit_tracker()
write_styles()

def build_token(sent, word, dc, domains):
    token = {**word.ctx, **group_by(domains)}
    # add_head(domains, dc, sent)
    if dc.governor != 0:
        head = sent.words[dc.governor - 1]
        token['head'] = head.ctx
    token['dc'] = dc.ctx
    return token

def get_aux_domain(sent):
    rs = []
    for word in filter(lambda w: w.upos == "AUX", sent.words):
        # dc=sent.words[word.governor-1]
        if word.governor == 0:
            # if the aux word is root; (这种情形会出现在德语依存分析中, 但在英语依存分析中是正常的)
            dc = word
            delegator = True
        else:
            dc = sent.words[word.governor - 1]
            delegator = False
        # print('℗', word.text, word.dependency_relation, word.governor, '☇' , dc.text)
        # print('\t', dc.index, dc.text, get_children_list(sent, dc))
        domains = []
        # stems = []
        # 需要收集的是aux单词依赖的对象的关联集, 而不是aux单词自身的关联集
        for c in filter(lambda w: equals(w.governor, dc.index), sent.words):
            # print('\t', c.index, c.text, get_children_list(sent, c))
            # domains.append((c.dependency_relation, c.index, c.text, c.lemma,
            #                 get_children_list(sent, c), get_word_features(c)))
            # add_domain(domains, stems, c, sent)
            c_domains = [w.ctx for w in children(c, sent)]
            domains.append({**c.ctx, **group_by(c_domains)})

        token=build_token(sent, word, dc, domains)
        rs.append(token)
        # rs.append({'type':'aux_domains', 'word': word.text, 'lemma':word.lemma,
        #           'rel': word.dependency_relation, 'governor': word.governor, 'head': dc.text,
        #           'head_pos': dc.upos.lower(), 'delegator':delegator,
        #           'index': word.index, 'domains': domains, 'stems':stems})
    return rs


def get_subj_domain(sent):
    rs = []
    for word in filter(lambda w: w.dependency_relation.endswith('subj'), sent.words):
        dc = sent.words[word.governor - 1]
        # print('℗', word.text, word.dependency_relation, word.governor, '☇' , dc.text)
        domains = []
        stems = []
        # 需要收集的是subj依赖的对象的关联集
        for c in filter(lambda w: equals(w.governor, dc.index), sent.words):
            # print('\t', c.index, c.text, get_children_list(sent, c))
            # domains.append((c.dependency_relation, c.index, c.text, c.lemma,
            #                 get_children_list(sent, c), get_word_features(c)))
            # add_domain(domains, stems, c, sent)
            c_domains = [w.ctx for w in children(c, sent)]
            domains.append({**c.ctx, **group_by(c_domains)})

        # add_head(domains, dc, sent)
        token = build_token(sent, word, dc, domains)
        rs.append(token)
        # rs.append({'type':'subj_domains', 'word': word.text, 'lemma':word.lemma,
        #           'rel': word.dependency_relation, 'governor': word.governor, 'head': dc.text,
        #           'head_pos': dc.upos.lower(), 'head_feats':[dc.lemma, dc.upos, dc.xpos],
        #           'index': word.index, 'domains': domains, 'stems':stems})
    return rs


class OperValue(object):

    def __init__(self, vtype=None, left=None, op=None, right=None, alias=None):
        self.alias = alias
        self._type = vtype
        self._left = left
        self._op = op
        self._right = right

    def __lt__(self, other):
        return OperValue(self._type, self._left, '$lt', other, self.alias)

    # //	__floordiv__(self, other)
    def __floordiv__(self, other):
        return OperValue(self._type, self, '$sub', other, self.alias)

    def __rshift__(self, other):
        return OperValue(self._type, self, '$for', other, self.alias)

    #     def __getattr__(self, name):
    #         if self._type:
    #             if self._left:
    #                 return value(self._type, '{0}.{1}'.format(self._left, name))
    #             else:
    #                 return value(self._type, name)
    #         else:
    #             return value(self.alias, name)
    def __call__(self, *args):
        return OperValue(self._type, self._left, op='predicate', right=args, alias=self.alias)


class Closure(object):
    def __getattr__(self, name):
        return OperValue(name)

def desc_expr(el, domains, lang):
    from sagas.nlu.inspector_wordnet import predicate

    if el._type.startswith('__'):
        comp='__'
        sub = el._type
        oper=el._type[2:]
    elif '_' in el._type:
        parts=el._type.split('_')
        comp=f"{parts[0]}'s {parts[1]}"
        sub=parts[0]
        oper=parts[1]
    else:
        comp=f"{el._type}'s lemma"
        sub=el._type
        oper='equals'
    val=', '.join(el._right)
    cond=eval_path(domains, sub)
    eq=lambda vals: any([v in vals for v in cond.split('/')])
    oper_mappings={'equals': eq,
                   'text': eq,
                   'cat': lambda vals: any([predicate(e, cond, lang, '*') for e in vals])
                   }
    if oper in oper_mappings:
        result=oper_mappings[oper](el._right)
        msg=''
    else:
        result=False
        msg=f'invalid operator {oper}'
    st.markdown(f"- `{comp}` {el._op} `{val}`, *{cond}* -> {result} {msg}")

    return result, msg

def eval_path(domains, path):
    from jsonpath_ng import jsonpath, parse

    if path.startswith('__'):
        return domains['lemma']+'/'+domains['text']
    else:
        prefix='$.'
        suffix='.text,lemma'
        parts=path.split('/')
        parts_str='.'.join([f"{t}[*]" for t in parts])
        expr= f"{prefix}{parts_str}{suffix}"
        parser=parse(expr)
        word = '/'.join([match.value for match in parser.find(domains)])
        return word

def predicate(domains, val, lang):
    results=[]
    st.markdown(f"*{val._left._type}* {val._left._op} {val._left._right}")
    results.append(desc_expr(val._left, domains, lang))

    # desc_expr(val._left)
    expr=val._right
    if isinstance(expr, list):
        for el in expr:
            results.append(desc_expr(el, domains, lang))
    else:
        results.append(desc_expr(expr, domains, lang))
    return results

def sure(doc, val):
    st.write('-' * 10)
    st.write(val._left._type, val._op, val._right._type)
    st.write(val._left._op, val._left._right, val._right._op, val._right._right)

ud = Closure()
def testing(doc, lang):
    # m = value('$m')
    # s = value('$s')
    # aux = value('$aux')
    # nsubj = value('$nsubj')

    # print(m.first._left)
    # st.write(aux._left, aux._type)
    # sure(aux('is') // nsubj('animal'))
    for el in doc:
        st.markdown(f"`{el['lemma']}` >> *{el['dc']['lemma']}*")
        r1=predicate(el, ud.__text('will') >> [ud.nsubj('what'), ud.dc_cat('weather')], lang)
        # r2=predicate(el, ud.__cat('be') >> [ud.nsubj('what'), ud.dc_cat('animal/object')], lang)
        st.write([r[0] for r in r1], all([r[0] for r in r1]))

    # sure(doc, ud.aux('is') // ud.nsubj('animal'))
    sure(doc, ud.aux('is') >> ud.nsubj('animal'))

def sidebar():
    cur_lang=display_lang_selector()

def parse_aux():
    lang = 'en'
    sents = 'what will be the weather in three days?'
    st.write(sents)
    data = {'lang': lang, "sents": sents, 'engine': cf.engine(lang)}
    doc_jsonify, resp = parse_sents(data)

    domains = get_aux_domain(doc_jsonify)
    testing(domains, 'en')

    # show analyse graph
    gv = display_doc_deps(doc_jsonify, resp)
    st.graphviz_chart(gv)

    st.write(domains)

def parse_subj():
    lang = 'ru'
    sents = 'Яблоко - это здоровый фрукт.'
    st.write(sents)
    data = {'lang': lang, "sents": sents, 'engine': cf.engine(lang)}
    doc_jsonify, resp = parse_sents(data)

    domains = get_subj_domain(doc_jsonify)
    testing(domains, 'ru')

    gv=display_doc_deps(doc_jsonify, resp)
    st.graphviz_chart(gv)

    st.write(domains)

def main():
    sidebar()
    st.subheader("Application")
    opt=st.sidebar.selectbox('Which fixture', ['parse subj', 'parse aux'])
    if opt=='parse subj':
        parse_subj()
    elif opt=='parse aux':
        parse_aux()

if __name__ == '__main__':
    main()

