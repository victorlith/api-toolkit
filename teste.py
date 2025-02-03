import asyncio
import time
from controllers.user_controller import *


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

    start_time = time.perf_counter()
    user = await rank_dos_usuarios_controller()
    print(user)
    end_time = time.perf_counter()

    print(end_time - start_time)


if __name__ == '__main__':
    asyncio.run(main())