import asyncio
import time
from models.exoplanet import *
from controllers.exoplanet_controller import *


async def main():
    #rank = []
    #user = await rank_dos_usuarios_controller()
    #for u in user:
        #usuario = {
            #'user_name': u['user_name'],
            #'level': u['level'],
            #'total_exp': u['total_exp']
        #}
        #rank.append(usuario)
    
    #print(rank)

    exoplanet = ExoplanetController()
    start_time = time.perf_counter()
    user = await exoplanet.filtrar_exoplanetas_v2(0, filtro='g')
    print(user)
    end_time = time.perf_counter()

    print('\nTempo de Execução: ', end_time - start_time)


if __name__ == '__main__':
    asyncio.run(main())