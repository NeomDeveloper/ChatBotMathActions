# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pprint import pprint
from json import dumps


class Explicacao(Action):

    def name(self) -> Text:
        return "explicando_algo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tema = tracker.get_slot('tema_para_ser_explicado')
        print('chega aqui =D')

        pprint(tracker.current_slot_values())
        pprint(tracker.slots)
        pprint(tracker.get_latest_entity_values('tema_para_ser_explicado').__str__())
        dispatcher.utter_message("select * from restaurants where cuisine='{0}' limit 1".format(tema))

        return []
