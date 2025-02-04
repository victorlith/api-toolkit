import math
from models.exoplanet import Exoplanet

class ExoplanetController:
    def __init__(self):
        self.__exoplanet_repository = Exoplanet()

    def calcular_luminosidade(self, lum):
        if lum:
            return 10 ** float(lum)
        else:
            return 0

    def calcular_zona_habitavel(self, luminosidade: float) -> float:
        if luminosidade:
            # Constantes para os limites interno e externo (relativo ao Sol)
            S_interno = 0.95
            S_externo = 1.37
            limite_interno = math.sqrt(luminosidade * S_interno)
            limite_externo = math.sqrt(luminosidade * S_externo)
            return limite_interno, limite_externo
        else:
            return None
        
    async def buscar_exoplaneta_v2(self, nome: str):       
        response = await self.__exoplanet_repository.buscar_exoplaneta_v2(nome)
        checar_valor = lambda x: None if x is None else x
        luminosidade: float = self.calcular_luminosidade(response[0]['st_lum'])
        zona_habitavel: float = self.calcular_zona_habitavel(luminosidade)
        response[0]['st_lum'] = luminosidade
        response[0]['pl_sy_zona_habitavel'] = zona_habitavel
        return response
    
    async def buscar_todos_exoplanetas_v2(self, offset: int):
        response = await self.__exoplanet_repository.buscar_todos_exoplanetas_v2(offset)
        return response
    
    async def pesquisar_por_exoplaneta_v2(self, nome: str) -> list:
        response = await self.__exoplanet_repository.pesquisar_por_exoplaneta_v2(nome)
        return response