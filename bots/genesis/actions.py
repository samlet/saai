# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

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

class ActionLogCommEvent(Action):
    """Revertible mapped action for utter_is_bot"""

    def name(self):
        return "action_log_commevent"

    def run(self, dispatcher: CollectingDispatcher,
            tracker:Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pprint(tracker.slots)
        dispatcher.utter_message(json_message={'result': 'log ok'})
        return [UserUtteranceReverted()]

