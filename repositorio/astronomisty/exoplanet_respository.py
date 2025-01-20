import sqlite3
from .exoplanet import Exoplanet

class ExoplanetRepository:
    def __init__(self):
        self.__conn = sqlite3.connect('repositorio/astronomisty/database/database_exoplanet.db')

    def buscar_exoplaneta(self, nome: str) -> [Exoplanet, None]:
        try:
            cursor = self.__conn.cursor()
            cursor.execute(f'SELECT pl_name, '
                           'ROUND(pl_bmasse, 2), '
                           'pl_rade, '
                           'ROUND(pl_orbper, 1), '
                           'disc_year, disc_pubdate, '
                           'discoverymethod, '
                           'hostname, '
                           'rastr, '
                           'decstr, '
                           'ROUND(sy_plx, 2), '
                           'ROUND(sy_dist * 3.26156, 2) as sy_dist_ly, '
                           'ROUND(sy_dist, 2), '
                           'st_mass, '
                           'st_rad, '
                           'st_teff, '
                           'st_spectype, '
                           'sy_pnum, '
                           f'sy_snum FROM PSCompPars_2025 WHERE pl_name = "{nome}"')

            response = cursor.fetchall()

            if response:
                exoplaneta = Exoplanet()

                for r in response:
                    exoplaneta.pl_nome = r[0]
                    exoplaneta.pl_massa = r[1]
                    exoplaneta.pl_raio = r[2]
                    exoplaneta.pl_orb_periodo = r[3]
                    exoplaneta.pl_ano_descoberta = r[4]
                    exoplaneta.pl_data_publicacao = r[5]
                    exoplaneta.pl_metodo_descoberta = r[6]
                    exoplaneta.pl_sy_nome = r[7]
                    exoplaneta.pl_sy_ascensao = r[8]
                    exoplaneta.pl_sy_declinacao = r[9]
                    exoplaneta.pl_sy_paralax = r[10]
                    exoplaneta.pl_sy_distancia_anos_luz = r[11]
                    exoplaneta.pl_sy_distancia_parsec = r[12]
                    exoplaneta.pl_sy_massa = r[13]
                    exoplaneta.pl_sy_raio = r[14]
                    exoplaneta.pl_sy_temperatura = r[15]
                    exoplaneta.pl_sy_tipo_espectral = r[16]
                    exoplaneta.pl_sy_num_exoplanetas = r[17]
                    exoplaneta.pl_sy_num_estrelas = r[18]

                return exoplaneta
            else:
                return None
        except Exception as e:
            print(f'Erro ao buscar exoplaneta: {e}')
        finally:
            self.__conn.close()

    def buscar_todos_exoplanetas(self, offset=0) -> [list, None]:
        try:
            cursor = self.__conn.cursor()
            cursor.execute(f'SELECT pl_name, '
                           'ROUND(pl_bmasse, 2), '
                           'pl_rade, pl_orbper, '
                           'disc_year, disc_pubdate, '
                           'discoverymethod, '
                           'hostname, '
                           'rastr, '
                           'decstr, '
                           'sy_plx, '
                           'ROUND(sy_dist * 3.26156, 2) as sy_dist_ly, '
                           'sy_dist, '
                           'st_mass, '
                           'st_rad, '
                           'st_teff, '
                           'st_spectype, '
                           'sy_pnum, '
                           f'sy_snum FROM PSCompPars_2025 WHERE pl_name IS NOT NULL ORDER BY pl_name LIMIT 10 OFFSET {offset} ')

            response = cursor.fetchall()

            exoplanetas = []
            for r in response:
                exoplaneta = Exoplanet()
                exoplaneta.pl_nome = r[0]
                exoplaneta.pl_massa = r[1]
                exoplaneta.pl_raio = r[2]
                exoplaneta.pl_orb_periodo = r[3]
                exoplaneta.pl_ano_descoberta = r[4]
                exoplaneta.pl_data_publicacao = r[5]
                exoplaneta.pl_metodo_descoberta = r[6]
                exoplaneta.pl_sy_nome = r[7]
                exoplaneta.pl_sy_ascensao = r[8]
                exoplaneta.pl_sy_declinacao = r[9]
                exoplaneta.pl_sy_paralax = r[10]
                exoplaneta.pl_sy_distancia_anos_luz = r[11]
                exoplaneta.pl_sy_distancia_parsec = r[12]
                exoplaneta.pl_sy_massa = r[13]
                exoplaneta.pl_sy_raio = r[14]
                exoplaneta.pl_sy_temperatura = r[15]
                exoplaneta.pl_sy_tipo_espectral = r[16]
                exoplaneta.pl_sy_num_exoplanetas = r[17]
                exoplaneta.pl_sy_num_estrelas = r[18]

                exoplanetas.append(exoplaneta.to_dic())

            return exoplanetas

        except Exception as e:
            print(f'{e}')
        finally:
            self.__conn.close()

    def pesquisar_por_exoplaneta(self, nome) -> [list, None]:
        try:
            cursor = self.__conn.cursor()
            cursor.execute(f'SELECT pl_name, '
                           'ROUND(pl_bmasse, 2), '
                           'pl_rade, '
                           'ROUND(pl_orbper, 1), '
                           'disc_year, disc_pubdate, '
                           'discoverymethod, '
                           'hostname, '
                           'rastr, '
                           'decstr, '
                           'ROUND(sy_plx, 2), '
                           'ROUND(sy_dist * 3.26156, 2) as sy_dist_ly, '
                           'ROUND(sy_dist, 2), '
                           'st_mass, '
                           'st_rad, '
                           'st_teff, '
                           'st_spectype, '
                           'sy_pnum, '
                           f'sy_snum FROM PSCompPars_2025 WHERE pl_name LIKE "{nome}%" ORDER BY pl_name ASC LIMIT 10')

            response = cursor.fetchall()

            if response:
                exoplanets = []

                for r in response:
                    exoplaneta = Exoplanet()
                    exoplaneta.pl_nome = r[0]
                    exoplaneta.pl_massa = r[1]
                    exoplaneta.pl_raio = r[2]
                    exoplaneta.pl_orb_periodo = r[3]
                    exoplaneta.pl_ano_descoberta = r[4]
                    exoplaneta.pl_data_publicacao = r[5]
                    exoplaneta.pl_metodo_descoberta = r[6]
                    exoplaneta.pl_sy_nome = r[7]
                    exoplaneta.pl_sy_ascensao = r[8]
                    exoplaneta.pl_sy_declinacao = r[9]
                    exoplaneta.pl_sy_paralax = r[10]
                    exoplaneta.pl_sy_distancia_anos_luz = r[11]
                    exoplaneta.pl_sy_distancia_parsec = r[12]
                    exoplaneta.pl_sy_massa = r[13]
                    exoplaneta.pl_sy_raio = r[14]
                    exoplaneta.pl_sy_temperatura = r[15]
                    exoplaneta.pl_sy_tipo_espectral = r[16]
                    exoplaneta.pl_sy_num_exoplanetas = r[17]
                    exoplaneta.pl_sy_num_estrelas = r[18]
                    exoplanets.append(exoplaneta.to_dic())
                return exoplanets
            else:
                return None
        except Exception as e:
            print(f'Erro ao buscar exoplaneta: {e}')
        finally:
            self.__conn.close()