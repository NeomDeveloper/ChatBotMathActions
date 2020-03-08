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

import requests
import json

URL_HOST_BASES = "http://localhost:8000/converter.php?"

URL_REQUEST_CONVERTER_BASES = URL_HOST_BASES + "valor={valor}&" \
                                               "base_valor={base_valor}&" \
                                               "base_conversao={base_converter}"


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


class ConverterBases(Action):
    def name(self) -> Text:
        return "converter_bases_action"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            dados = Helper.getValores(tracker)

            txt = "Ok, convertendo {valor} de {base_valor} para {base_converter}".format(
                valor=dados['valor'],
                base_valor=dados['base_valor'],
                base_converter=dados['base_converter'],
            )

            dispatcher.utter_message(txt)

            url_response = requests.get(
                URL_REQUEST_CONVERTER_BASES.format(
                    valor=dados['valor'], base_valor=dados['base_valor'], base_converter=dados['base_converter'],
                ))

            response_json = json.loads(url_response.text)

            if response_json['status'] == "success":
                response = response_json['response']
                resposta = response['resposta']
                explicacao = response['explicacao']

                dispatcher.utter_message("O {valor} de {base_valor} para {base_converter} é: {resposta}".format(
                    valor=dados['valor'],
                    base_valor=dados['base_valor'],
                    base_converter=dados['base_converter'],
                    resposta=resposta
                ))

                dispatcher.utter_message("Quer entender? Te explico ")

                dispatcher.utter_message("{explicacao}".format(
                    explicacao=explicacao
                ))
            else:
                dispatcher.utter_message(response_json['erro'])

        except Exception as e:
            dispatcher.utter_message(
                "Alguma informação ficou errada =/. Por favor digite da seguinte forma:"
                " 'converter {valor} {tipo de base do valor} para {base que deseja converter}'" + str(e)
            )

        return []


class InicioEnsinoConverterBases(Action):
    def name(self) -> Text:
        return "inicio_ensino_converter_bases_action"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Ok, vamos lá")

        dispatcher.utter_message(
            " Podemos considerar, a fim de simplificação, que base numérica é "
            "um conjunto de símbolos (ou algarismos) com o qual podemos"
            " representar uma certa quantidade ou número."

        )

        dispatcher.utter_message(
            "No dia a dia costuma-se utilizar a base dez, ou base decimal, que como o "
            "próprio nome já diz é composta por 10 algarismos diferentes:  0, 1, 2, 3, 4, 5, 6, 7, 8 e 9."
            "  Dessa forma, uma sequência de contagem para a base decimal pode ser expressa através da "
            "seguinte sequência de números:"
            "0          1          2          3          4          5          6          7          8          9"
        )

        dispatcher.utter_message(
            "Dado que o algarismo ‘9’ é o algarismo de maior valor numérico disponível nessa base, "
            "para poder representar um número ma    ior do que 9 é necessário adicionar mais um dígito "
            "ao número original, sendo que esse dígito deve ter um peso igual ao peso do número "
            "representado até então mais um. Para o caso da base decimal, se o último número"
            " representado foi 9 então o peso do próximo dígito é 9 + 1 = 10, o que leva a:"
            "10         11         12         13         …        97         98         99"
        )

        dispatcher.utter_message(
            "As possibilidades esgotaram-se novamente, e todos os dígitos do número já apresentam o "
            "algarismo de maior valor numérico. Mais uma vez, deve ser adicionado um dígito extra ao "
            "número, sendo o seu peso igual a 99 + 1 = 100  e gerando então:"
            "100       101       …"
        )

        dispatcher.utter_message("Fonte: http://www.dainf.cefetpr.br/~robson/prof/aulas/common/bases.htm")

        return []


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
        return {
            "valor": next(traker.get_latest_entity_values('valor')),
            "base_valor": next(traker.get_latest_entity_values('base_valor')),
            "base_converter": next(traker.get_latest_entity_values('base_para_converter'))
        }
