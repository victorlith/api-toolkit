from .exoplanet_service import ExoplanetService
from .exoplanet import Exoplanet

class ExoplanetController:
    def __init__(self):
        self.__exoplanet_service = ExoplanetService()

    def buscar_exoplaneta(self, nome: str) -> Exoplanet:
        return self.__exoplanet_service.buscar_exoplaneta(nome)

    def buscar_todos_exoplanetas(self, offset: int) -> list:
        return self.__exoplanet_service.buscar_todos_exoplanetas(offset)