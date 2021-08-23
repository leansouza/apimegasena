from typing import Dict, Tuple

from app.main.util.decorator import admin_token_required
from flask import request
from flask_restx import Resource

from ..service.game_service import (save_new_game, get_by_game_by_user)

from ..util.dto import GameDto
from ..util.scrapping import get_results


NUMERO_DEZENAS = 6

api = GameDto.api
_game = GameDto.user


@api.route('/<ticketgame_id>')
@api.param('ticketgame_id', 'The ticket game identifier')
@api.response(404, 'Ticket game not found.')
class User(Resource):
    @api.doc('get a ticket game')
    @admin_token_required
    @api.marshal_with(_game)
    def get(self, public_id):
        """get a user given its identifier"""
        list_dozens = get_by_game_by_user(public_id)
        if not list_dozens:
            return api.abort(404)
        else:
            result_megasena = get_results()
            total_result = []
            for i in result_megasena:
                for j in list_dozens:
                    if i == j:
                        total_result.append(i)
            if len(total_result) >= 4:
                 response_object = {'Você acertou o número mínimo de combinações: ': total_result}
                 return response_object, 409
                
            else:
                response_object = {
                                    'Segue os resultados da mega sena': result_megasena,
                                    'Seus resultados ': list_dozens
                                 }


def existeNumero(numeros, n): 
    return n in numeros

def contaAcertos(sorteio, aposta):
    global NUMERO_DEZENAS
    acertos = 0
    for i in range(0, NUMERO_DEZENAS):
        nroAposta = aposta[i]

        # compara cada nro apostado com os sorteados
        if (existeNumero(sorteio, nroAposta)):
            acertos += 1

    return acertos