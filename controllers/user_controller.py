from models.user import *


async def buscar_usuario_controller(user_id: int):
    data_user = await buscar_usuario_v2(user_id)
    return data_user


async def rank_dos_usuarios_controller():
    users_rank = await rank_de_usuarios()
    return users_rank