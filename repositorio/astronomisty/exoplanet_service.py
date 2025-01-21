import math

from .exoplanet_respository import ExoplanetRepository
from .exoplanet import Exoplanet

class ExoplanetService:
    def __init__(self):
        self.__exoplanet_repository = ExoplanetRepository()

    def buscar_exoplaneta(self, nome: str) -> Exoplanet:
        response = self.__exoplanet_repository.buscar_exoplaneta(nome)
        if response:
            exoplaneta = Exoplanet()

            checar_valor = lambda x: None if x is None else x

            for r in response:

                exoplaneta.pl_nome = r[0]
                exoplaneta.pl_massa = r[1]
                exoplaneta.pl_raio = r[2]
                exoplaneta.pl_densidade = checar_valor(r[3]) * 1000
                exoplaneta.pl_orb_periodo = r[4]
                exoplaneta.pl_ano_descoberta = r[5]
                exoplaneta.pl_data_publicacao = r[6]
                exoplaneta.pl_metodo_descoberta = r[7]
                exoplaneta.pl_sy_nome = r[8]
                exoplaneta.pl_sy_ascensao = r[9]
                exoplaneta.pl_sy_declinacao = r[10]
                exoplaneta.pl_sy_paralax = r[11]
                exoplaneta.pl_sy_distancia_anos_luz = r[12]
                exoplaneta.pl_sy_distancia_parsec = r[13]
                exoplaneta.pl_sy_massa = r[14]
                exoplaneta.pl_sy_raio = r[15]
                exoplaneta.pl_sy_temperatura = r[16]
                exoplaneta.pl_sy_tipo_espectral = r[17]
                exoplaneta.pl_sy_num_exoplanetas = r[18]
                exoplaneta.pl_sy_num_estrelas = r[19]
                exoplaneta.pl_sy_luminosidade =  self.calcular_luminosidade(checar_valor(r[20]))
                exoplaneta.pl_sy_zona_habitavel = self.calcular_zona_habitavel(exoplaneta.pl_sy_luminosidade)

            return exoplaneta.to_dic()

    def buscar_todos_exoplanetas(self, offset: int) -> list:
        response = self.__exoplanet_repository.buscar_todos_exoplanetas(offset)
        exoplanetas = []
        for r in response:
            exoplaneta = Exoplanet()
            exoplaneta.pl_nome = r[0]
            exoplaneta.pl_massa = r[1]
            exoplaneta.pl_sy_distancia_anos_luz = r[2]
            exoplanetas.append(exoplaneta.to_dic())
        return exoplanetas

    def pesquisar_por_exoplaneta(self, nome: str):
        response = self.__exoplanet_repository.pesquisar_por_exoplaneta(nome)
        if response:
            exoplanets = []

            for r in response:
                exoplaneta = Exoplanet()
                exoplaneta.pl_nome = r[0]
                exoplaneta.pl_massa = r[1]
                exoplaneta.pl_sy_distancia_anos_luz = r[2]
                exoplanets.append(exoplaneta.to_dic())
            return exoplanets

    def calcular_luminosidade(self, lum):
        if lum:
            return 10 ** float(lum)
        else:
            return None

    def calcular_zona_habitavel(self, luminosidade: float):
        if luminosidade:
            # Constantes para os limites interno e externo (relativo ao Sol)
            S_interno = 0.95
            S_externo = 1.37
            limite_interno = math.sqrt(luminosidade * S_interno)
            limite_externo = math.sqrt(luminosidade * S_externo)
            return limite_interno, limite_externo
        else:
            return None