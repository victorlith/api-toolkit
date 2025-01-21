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
                           'pl_dens,'
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
                           f'sy_snum, '
                           f'st_lum FROM PSCompPars_2025 WHERE pl_name = "{nome}"')

            response = cursor.fetchall()
            return response
        except Exception as e:
            print(f'Erro ao buscar exoplaneta: {e}')
        finally:
            self.__conn.close()

    def buscar_todos_exoplanetas(self, offset=0) -> [list, None]:
        try:
            cursor = self.__conn.cursor()
            cursor.execute(f'SELECT pl_name, '
                           f'ROUND(pl_bmasse, 2), '
                           f'ROUND(sy_dist * 3.26156, 2) as sy_dist_ly '
                           f'FROM PSCompPars_2025 WHERE pl_name IS NOT NULL ORDER BY pl_name ASC LIMIT 10 OFFSET {offset}')
            response = cursor.fetchall()
            return response
        except Exception as e:
            print(f'{e}')
        finally:
            self.__conn.close()

    def pesquisar_por_exoplaneta(self, nome) -> [list, None]:
        try:
            cursor = self.__conn.cursor()
            cursor.execute(f'SELECT pl_name, ROUND(pl_bmasse, 2), ROUND(sy_dist * 3.26156, 2) as sy_dist_ly FROM PSCompPars_2025 WHERE pl_name LIKE "{nome}%" ORDER BY pl_name ASC LIMIT 10')
            response = cursor.fetchall()
            return response
        except Exception as e:
            print(f'Erro ao buscar exoplaneta: {e}')
        finally:
            self.__conn.close()