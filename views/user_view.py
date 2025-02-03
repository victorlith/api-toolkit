from flask import Blueprint, request, jsonify
from controllers.user_controller import rank_dos_usuarios_controller, buscar_usuario_controller


user_bp = Blueprint("user", __name__)


@user_bp.route('/v2/economisty/user-data', methods=['GET'])
async def buscar_usuario_view():
    id_user = request.args.get('id_user', type=int)
    if id_user is not None:
        
        data_user = await buscar_usuario_controller(id_user)
        
        if data_user:
            return jsonify({"resultado": dict(data_user)})
        else:
            return jsonify({"id_user": id_user, "resultado": "ID não encontrado"})
    else:
        return jsonify({"erro": "ID não fornecido"}), 400

@user_bp.route('/v2/economisty/ranking', methods=['GET'])
async def ranking_usuarios_view():
    ranking = await rank_dos_usuarios_controller()
    return jsonify(ranking)