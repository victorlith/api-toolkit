from .exoplanet_respository import ExoplanetRepository
from .exoplanet import Exoplanet

class ExoplanetService:
    def __init__(self):
        self.__exoplanet_repository = ExoplanetRepository()

    def buscar_exoplaneta(self, nome: str) -> Exoplanet:
        return self.__exoplanet_repository.buscar_exoplaneta(nome)

    def buscar_todos_exoplanetas(self, offset: int) -> list:
        return self.__exoplanet_repository.buscar_todos_exoplanetas(offset)