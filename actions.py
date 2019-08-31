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


class HexadecimalParaDecimal(Action):

    def name(self) -> Text:
        return "converter_hexa_para_decimal"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        valores = Helper.getValores(tracker)

        dispatcher.utter_message("Converter {0} para {1}".format(valores[0], valores[1]))

        return []


class HexadecimalParaBinario(Action):

    def name(self) -> Text:
        return "converter_hexa_para_binario"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        valores = Helper.getValores(tracker)

        dispatcher.utter_message("Converter {0} para {1}".format(valores[0], valores[1]))

        return []


class DecimalParaHexadecimal(Action):

    def name(self) -> Text:
        return "converter_decimal_para_hexa"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        valores = Helper.getValores(tracker)

        dispatcher.utter_message("Converter {0} para {1}".format(valores[0], valores[1]))

        return []


class DecimalParaBinario(Action):
    def name(self) -> Text:
        return "converter_decimal_para_binario"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        valores = Helper.getValores(tracker)

        dispatcher.utter_message("Converter {0} para {1}".format(valores[0], valores[1]))

        return []


class BinarioParaHexadecimal(Action):
    def name(self) -> Text:
        return "converter_binario_para_hexa"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        valores = Helper.getValores(tracker)

        dispatcher.utter_message("Converter {0} para {1}".format(valores[0], valores[1]))

        return []


class BinarioParaDecimal(Action):
    def name(self) -> Text:
        return "converter_binario_para_decimal"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        valores = Helper.getValores(tracker)

        dispatcher.utter_message("Converter {0} para {1}".format(valores[0], valores[1]))

        return []


class Explicacao(Action):

    def name(self) -> Text:
        return "explicando_algo"

    @staticmethod
    def required_slots(tracker):
        return ["tema_para_ser_explicado"]

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tema = next(tracker.get_latest_entity_values('tema_para_ser_explicado'))

        print(tema)
        print(tracker.latest_message.items())

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


class Entendeu(Action):

    def name(self) -> Text:
        return "entendeu_sobre_o_tema"

    @staticmethod
    def required_slots(tracker):
        return ["tema_para_ser_explicado"]

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tema = tracker.get_slot('tema_para_ser_explicado')

        if tema not in Explicacao.required_slots(tracker):
            dispatcher.utter_message(
                "Desculpe, parece que alguma coisa nao esta certa =/"
            )
            return []

        print(tema)

        dispatcher.utter_message("Que bom que vc entendeu sobre: {0}... ".format(tema))

        if not tema.strip():
            # Só colocar o slot se o tema não estiver vazio =D
            return [SlotSet('tema_para_ser_explicado', tema)]

        return []


class NaoEntendeu(Action):

    def name(self) -> Text:
        return "nao_entendeu_sobre_o_tema"

    @staticmethod
    def required_slots(tracker):
        return ["tema_para_ser_explicado"]

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tema = tracker.get_slot('tema_para_ser_explicado')

        if tema not in Explicacao.required_slots(tracker):
            dispatcher.utter_message(
                "Desculpe, parece que alguma coisa nao esta certa =/"
            )
            return []

        print(tema)

        dispatcher.utter_message("Que pena que vc nao entendeu sobre: {0}... ".format(tema))

        if not tema.strip():
            # Só colocar o slot se o tema não estiver vazio =D
            return [SlotSet('tema_para_ser_explicado', tema)]

        return []


class Helper:

    @staticmethod
    def getValores(traker: Tracker):
        return [
            next(traker.get_latest_entity_values('valor_para_converter')),
            next(traker.get_latest_entity_values('base_para_conversao'))
        ]
