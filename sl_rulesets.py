import streamlit as st
from durable.engine import Host

from interacts.common import display_lang_selector
from interacts.sl_utils import all_labels, write_styles
from interacts.tracker_streamlit import enable_streamlit_tracker

from durable.lang import *
import durable.lang as dlang

enable_streamlit_tracker()
write_styles()

with ruleset('wordnet'):
    @when_all(m.subject.matches('.*thing.*, entity.*'))
    def matches(c):
        st.write('string matches pat -> {0}'.format(c.m.subject))


    @when_all(m.amod.anyItem(item.matches('.*thing.*, entity.*')))
    def amod_with(c):
        st.write('amod pat -> {0}'.format(c.m.amod))


    @when_all(m.subject.imatches('.*thing.*'))
    def contains(c):
        st.write('string contains pat -> {0}'.format(c.m.subject))

def sidebar():
    cur_lang=display_lang_selector()

def rule_test():
    host = Host()
    ruleset_definitions = {}
    for name, rset in dlang._rulesets.items():
        full_name, ruleset_definition = rset.define()
        ruleset_definitions[full_name] = ruleset_definition

    host.register_rulesets(ruleset_definitions)
    # assert_fact
    host.post('wordnet', {'subject': 'main.n.01, body_of_water.n.01, thing.n.12, physical_entity.n.01, entity.n.01'})
    host.post('wordnet', {'amod': ['main.n.01, body_of_water.n.01, thing.n.12, physical_entity.n.01, entity.n.01']})

def main():
    sidebar()
    st.subheader("Application")
    rule_test()

if __name__ == '__main__':
    main()

