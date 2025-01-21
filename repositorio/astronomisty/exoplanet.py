
class Exoplanet:
    def __init__(self):
        self.pl_nome = None
        self.pl_massa = 0
        self.pl_raio = None
        self.pl_densidade = 0
        self.pl_orb_periodo = None
        self.pl_ano_descoberta = None
        self.pl_data_publicacao = None
        self.pl_metodo_descoberta = None
        self.pl_sy_nome = None
        self.pl_sy_ascensao = None
        self.pl_sy_declinacao = None
        self.pl_sy_paralax = None
        self.pl_sy_distancia_anos_luz = None
        self.pl_sy_distancia_parsec = None
        self.pl_sy_massa = None
        self.pl_sy_raio = None
        self.pl_sy_luminosidade = 0
        self.pl_sy_temperatura = 0
        self.pl_sy_tipo_espectral = None
        self.pl_sy_num_exoplanetas = None
        self.pl_sy_num_estrelas = None
        self.pl_sy_zona_habitavel = 0

    def to_dic(self):
        return self.__dict__