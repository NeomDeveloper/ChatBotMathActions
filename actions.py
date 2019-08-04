# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class Explicacao(Action):

    def name(self) -> Text:
        return "explicando_algo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tema = tracker.get_slot('tema_para_ser_explicado')
        dispatcher.utter_message("select * from restaurants where cuisine='{0}' limit 1".format(tema))

        return []
