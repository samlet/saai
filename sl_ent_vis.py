import streamlit as st

from interacts.common import display_lang_selector
from interacts.sl_utils import all_labels, write_styles
from interacts.tracker_streamlit import enable_streamlit_tracker

from saai.ner_jieba import extract_entities
from sl_utils import HTML_WRAPPER

enable_streamlit_tracker()
write_styles()

def sidebar():
    cur_lang=display_lang_selector()

def ent_vis(text):
    from ipymarkup.palette import palette, BLUE, RED, GREEN
    from ipymarkup import box_markup
    spans = [(w['start'], w['end'], w['entity']) for w in extract_entities(text)]
    markup=box_markup(text, spans, palette=palette(PER=BLUE, ORG=RED, LOC=GREEN))
    html=''
    for line in markup.as_html:
        html=html+line
    # Newlines seem to mess with the rendering
    # html = html.replace("\n", " ")
    st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)

DEFAULT_TEXT = 'Rami Eid正在纽约石溪大学学习'
def main():
    sidebar()
    st.subheader("entity visualizer")
    text = st.text_area("Text to analyze", DEFAULT_TEXT)
    ent_vis(text)

if __name__ == '__main__':
    main()

