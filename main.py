from flask import Flask, jsonify, request
import repositorio.economisty.module_utils as module_utils
from bson import json_util
from repositorio.astronomisty.exoplanet_controller import ExoplanetController
from repositorio.astronomisty.exoplanet_service import ExoplanetService
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

pattern_route = 'api'

@app.route(f'/{pattern_route}/economisty/user-data', methods=['GET'])
async def find_user():
    id_user = request.args.get('id_user', type=int)
    if id_user is not None:
        id_user = int(id_user)

        collection = await module_utils.find_db_collection('users')
        data_user = await collection.find_one({"user_id": id_user})
        pipeline = [
            {"$setWindowFields": {"sortBy": {"total_exp": -1}, "output": {"rank": {"$rank": {}}}}},
            {"$match": {"user_id": data_user["user_id"]}}
        ]
        rank = await collection.aggregate(pipeline).to_list()

        if data_user:
            return json_util.dumps({"id_user": id_user, "resultado": data_user, "rank": rank[0]["rank"]})
        else:
            return jsonify({"id_user": id_user, "resultado": "ID não encontrado"})
    else:
        return jsonify({"erro": "ID não fornecido"}), 400

@app.route(f'/{pattern_route}/economisty/checar-cooldown', methods=['GET'])
async def cooldown():
    user_id = int(request.args.get('user-id'))
    if user_id:
        response = await module_utils.checar_cooldown(user_id)
        return jsonify({"user_id": user_id, "response_cooldown": response})
    else:
        return jsonify({"erro": "ID não fornecido"}), 400

@app.route(f'/{pattern_route}/economisty/update-cooldown', methods=['GET'])
async def update_cooldown():
    user_id = int(request.args.get('user-id'))
    if user_id:
        await module_utils.atualizar_cooldown(user_id)
        return '', 204
    return 'ID nao fornecido', 400

@app.route(f'/{pattern_route}/economisty/resgatar-moedas', methods=['GET'])
async def resgatar_moedas():
    user_id = int(request.args.get('user-id'))
    exp = 80
    if user_id:
        data_user = await module_utils.buscar_usuario(user_id)
        response = await module_utils.evento_moedas(data_user["cargo"]["salario"], exp, user_id)

        if response[3] is True:
            await module_utils.alterar_saldo(user_id, response[0])
            level_up = await module_utils.adicionar_exp(user_id, response[1])
            return json_util.dumps({"user_id": user_id, "response": response, "evento": True, "level_up": level_up})
        else:
            await module_utils.alterar_saldo(user_id, response[0])
            level_up = await module_utils.adicionar_exp(user_id, response[1])
            return json_util.dumps({"user_id": user_id, "response": [data_user["cargo"]["salario"], exp], "evento": False, "level_up": level_up})

@app.route(f'/{pattern_route}/economisty/ranking', methods=['GET'])
async def ranking_usuarios():
    ranking = await module_utils.rank_de_usuarios()
    ranking_list = []
    for idx, r in enumerate(ranking, 1):
        ranking_list.append({'rank': idx,
                             'nome': r['user_name'],
                             'nivel': r['level'],
                             'total_exp': r['total_exp']})

    return jsonify(ranking_list)

@app.route(f'/{pattern_route}/astronomisty/exoplanet/<name>', methods=['GET'])
async def buscar_exoplaneta(name):
    exoplanet_controller = ExoplanetController()
    response = exoplanet_controller.buscar_exoplaneta(name)

    if response:
        return jsonify({"resultado": response})
    else:
        return jsonify({"resultado": None}), 400

@app.route(f'/{pattern_route}/astronomisty/allExoplanets' ,methods=['GET'])
async def buscar_todos_exoplanetas():
    offset = request.args.get('offset', default=0, type=int)
    exoplanet_controller = ExoplanetController()
    response = exoplanet_controller.buscar_todos_exoplanetas(offset)

    if response:
        return jsonify({"resultado": response})
    else:
        return jsonify({"resultado": None}), 400

@app.route(f'/{pattern_route}/astronomisty/search/<nome>', methods=['GET'])
async def pesquisar_exoplaneta(nome):
    if nome:
        exoplanet_controller = ExoplanetController()
        response = exoplanet_controller.pesquisar_por_exoplaneta(nome)

        if response:
            return jsonify({'resultado': response})
        else:
            return jsonify({'resultado': None, 'msg': f'O exoplaneta com o nome ({nome}) não foi encontrado.'})
    else:
        return jsonify({'resultado': 'Nome do exoplaneta não fornecido'})


@app.route(f'/{pattern_route}/v2/astronomisty/exoplanet/<nome>', methods=['GET'])
async def buscar_exoplaneta_v2(nome):
    exoplanet_service = ExoplanetService()
    response = await exoplanet_service.buscar_exoplaneta_v2_service(nome)

    if response:
        return jsonify(response[0])
    else:
        return jsonify(None), 400
    
@app.route(f'/{pattern_route}/v2/astronomisty/search/<nome>', methods=['GET'])
async def pesquisar_exoplaneta_v2(nome):
    if nome:
        exoplanet_service = ExoplanetService()
        response = await exoplanet_service.pesquisar_por_exoplaneta_v2_service(nome)

        if response:
            return jsonify(response)
        else:
            return jsonify({'resultado': None, 'msg': f'O exoplaneta com o nome ({nome}) não foi encontrado.'})
    else:
        return jsonify({'resultado': 'Nome do exoplaneta não fornecido'})

@app.route(f'/{pattern_route}/v2/astronomisty/allExoplanets', methods=['GET'])
async def buscar_todos_exoplanetas_v2():
    offset = request.args.get('offset', default=0, type=int)
    exoplanet_service = ExoplanetService()
    response = await exoplanet_service.buscar_todos_exoplanetas_v2_service(offset)

    if response:
        return jsonify(response)
    else:
        return jsonify(None), 400



if __name__ == '__main__':
    module_utils.carregar_eventos_moedas()
    app.run(host='0.0.0.0', port=80, debug=True)