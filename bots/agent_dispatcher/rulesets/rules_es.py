from typing import Text, Dict, Any

from sagas.nlu.rules_header import *

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_es(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_en prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ se 'I want to play music.'
            # pat(5, name='behave_media').verb(pred_any_path('xcomp/obj', 'sound/perception', 'n')),
            # $ ses '¿Te duelen las piernas?' (zh="你的腿受伤了吗？")
            pat(5, name='hurt_if').verb(behaveof('suffer', 'v'), nsubj=kindof('body_part', 'n')),
        ])

    def aux_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ se 'what will be the weather in three days?'
            # pat(5, name='query_weather').root(predict_aux(
            #     ud.__text('will') >> [ud.nsubj('what'), ud.dc_cat('weather')])),
            # 匹配继承链:
            # $ ses 'Este juego es facilísimo.' ([en] This game is very easy.)
            pat(5, name='desc_act').aux('adj', nsubj=kindof('activity', 'n')),
        ])

    def execute(self):
        if len(self.matched) > 0:
            matched_info = {k: len(v.results) for k, v in self.matched.items()}
            tc.emp('green', f"♯ matched id rules: {matched_info}")

