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

        tema = next(tracker.get_latest_entity_values('tema_para_ser_explicado')) if next(tracker.get_latest_entity_values('tema_para_ser_explicado')) else ''
        # print('chega aqui =D')

        dispatcher.utter_message(
            "Ok, vou pesquisar mais sobre {0}".format(tema)
        )

        dispatcher.utter_message(
            " Agora fazer alguma busca sobre {0} ".format(tema)
        )

        dispatcher.utter_message(
            "Conseguiu entender ? "
        )

        dispatcher.utter_button_message('entendeu?', List[domain])

        return []
