from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
from pprint import pprint

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Hello World!")

        return []

class ActionIsBot(Action):
    """Revertible mapped action for utter_is_bot"""

    def name(self):
        return "action_is_bot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker:Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pprint(tracker.slots)
        dispatcher.utter_template("utter_iamabot", tracker)
        return [UserUtteranceReverted()]

def prop(tracker:Tracker, attr:Text):
    attr_val = tracker.get_slot(attr) if attr in tracker.slots else ''
    return attr_val

class ActionLogCommEvent(Action):
    def name(self):
        return "action_log_commevent"

    def run(self, dispatcher: CollectingDispatcher,
            tracker:Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pprint(tracker.slots)
        dispatcher.utter_message(json_message={'result': 'log ok',
                                               'sents':prop(tracker, 'sents')})
        return [UserUtteranceReverted()]

class ActionPerformSound(Action):
    def name(self):
        return "action_perform_sound"

    def run(self, dispatcher: CollectingDispatcher,
            tracker:Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pprint(tracker.slots)
        dispatcher.utter_message(json_message={'result': 'success',
                                               'music_list': ['first song', 'second song'],
                                               'sents':prop(tracker, 'sents')})
        return [UserUtteranceReverted()]

