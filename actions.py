# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, UserUtteranceReverted, ConversationPaused


class Explicacao(Action):

    def name(self) -> Text:
        return "explicando_algo"

    @staticmethod
    def required_slots(tracker):
        return ["tema_para_ser_explicado"]

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # tema = tracker.get_slot('tema_para_ser_explicado')
        tema = next(tracker.get_latest_entity_values('tema_para_ser_explicado'))

        print(tema)

        # if tema not in Explicacao.required_slots(tracker):
        #     dispatcher.utter_message(
        #         "Desculpe, parece ainda não sei sobre esse tema =/"
        #     )
        #     return []

        dispatcher.utter_message("Ok, pesquisando sobre {0}... ".format(tema))

        dispatcher.utter_message(self.explicar(tema))

        dispatcher.utter_message("Conseguiu entender?")
        if not tema.strip():
            # Só colocar o slot se o tema não estiver vazio =D
            return [SlotSet('tema_para_ser_explicado', tema)]

        return []

    def explicar(self, tema):
        return 'Aqui a função para pesquisar sobre: ' + tema
