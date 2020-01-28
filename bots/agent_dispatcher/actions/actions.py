from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import json
import logging
logger = logging.getLogger(__name__)

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


class ActionPerformMedia(Action):
    def name(self):
        return "action_perform_media"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logging.info(json.dumps(tracker.current_slot_values(), indent=2, ensure_ascii=False))
        prop = lambda attr: tracker.get_slot(attr) if attr in tracker.slots else ''
        object_type=tracker.get_slot('object_type')
        dispatcher.utter_message(json_message={'result': 'success',
                                               'media_list': ['first song', 'second song'],
                                               'media_type': object_type,
                                               'sents': prop('sents')})
        # return [SlotSet("media_type", object_type)]
        return []


class ActionListProducts(Action):
    def name(self):
        return "action_list_products"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logger.info(json.dumps(tracker.current_slot_values(), indent=2, ensure_ascii=False))

        entities = tracker.latest_message.get("entities", [])
        entity_type='verb_domains'
        additional_info=next(x.get("additional_info") for x in entities if x.get("entity") == entity_type)
        logger.info(json.dumps(additional_info, indent=2, ensure_ascii=False))

        dispatcher.utter_message(json_message={'result': 'success',
                                               'product_list': ['first prod', 'second prod'],
                                               })
        return []
