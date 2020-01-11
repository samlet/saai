import streamlit as st

from interacts.common import display_lang_selector
from interacts.sl_utils import all_labels, write_styles
from interacts.tracker_streamlit import enable_streamlit_tracker
import requests
from sl_utils import HTML_WRAPPER

# from sl_ent_vis import ent_vis

enable_streamlit_tracker()
write_styles()

def sidebar(sender):
    from saai.saai_bot_cli import SaaiBotCli

    cur_lang=display_lang_selector()
    opt=st.sidebar.selectbox('Functions', ['nlu parse', 'bot talk'])
    if st.sidebar.button("reset conversation"):
        SaaiBotCli().reset_conversation(sender=sender)
    return cur_lang, opt

DEFAULT_TEXT = '感觉发烧了，该去哪个诊所哪个科室呢'

def talk(sents, sender='default'):
    response = requests.post(f'http://localhost:5005/webhooks/rest/webhook', json={'message': sents, 'sender':sender})
    print('status code:', response.status_code)
    return response.json()

def nlu_vis(sents):
    from ipymarkup import box_markup
    from saai.tool import rasa_nlu_parse

    result=rasa_nlu_parse(sents)
    ents = result['entities']
    spans = [(w['start'], w['end'], w['entity']) for w in ents]
    markup = box_markup(sents, spans)
    html = ''
    for line in markup.as_html:
        html = html + line
    # Newlines seem to mess with the rendering
    # html = html.replace("\n", " ")
    st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)
    st.write(result['intent'])

def bot_talk(sents, sender='default'):
    result=talk(sents, sender)
    st.markdown(f"**你说**  `{sents}`")
    st.write(result)

def main():
    sender='default'
    st.header("bot interact")
    lang, opt=sidebar(sender)

    if opt=='nlu parse':
        st.subheader("nlu parse")
        text = st.text_area("Text to analyze", DEFAULT_TEXT)
        nlu_vis(text)
    elif opt=='bot talk':
        st.subheader("nlu parse")
        text = st.text_input("Text to send", '你好')
        bot_talk(sents=text, sender=sender)

if __name__ == '__main__':
    main()

