from flask import Blueprint, jsonify, request
from controllers.exoplanet_controller import ExoplanetController


exoplanet_bp = Blueprint("exoplanet", __name__)


@exoplanet_bp.route(f'/v2/astronomisty/exoplanet/<nome>', methods=['GET'])
async def buscar_exoplaneta_v2(nome):
    exoplanet_controller = ExoplanetController()
    response = await exoplanet_controller.buscar_exoplaneta_v2(nome)

    if response:
        return jsonify(response[0])
    else:
        return jsonify(None), 400
    
@exoplanet_bp.route(f'/v2/astronomisty/search/<nome>', methods=['GET'])
async def pesquisar_exoplaneta_v2(nome):
    if nome:
        exoplanet_controller = ExoplanetController()
        response = await exoplanet_controller.pesquisar_por_exoplaneta_v2(nome)

        if response:
            return jsonify(response)
        else:
            return jsonify({'resultado': None, 'msg': f'O exoplaneta com o nome ({nome}) não foi encontrado.'})
    else:
        return jsonify({'resultado': 'Nome do exoplaneta não fornecido'})

@exoplanet_bp.route(f'/v2/astronomisty/allExoplanets', methods=['GET'])
async def buscar_todos_exoplanetas_v2():
    offset = request.args.get('offset', default=0, type=int)
    exoplanet_controller = ExoplanetController()
    response = await exoplanet_controller.buscar_todos_exoplanetas_v2(offset)

    if response:
        return jsonify(response)
    else:
        return jsonify(None), 400


@exoplanet_bp.route(f'/v2/astronomisty/filtrarExoplaneta', methods=['GET'])
async def filtrar_exoplaneta():
    offset = request.args.get('offset', default=0, type=int)
    filtro = request.args.get('filter', default=None, type=str)

    exoplanet_controller = ExoplanetController()
    response = await exoplanet_controller.filtrar_exoplanetas_v2(offset, filtro)

    if response:
        return jsonify(response)
    else:
        return jsonify(None), 400