from database.database_conn import DatabaseConnection


class Exoplanet:
    def __init__(self):
        self.__conn2 = DatabaseConnection().postgre_db()

    async def buscar_exoplaneta_v2(self, nome: str) -> list:
        db = await self.__conn2
        try:
            row = await db.fetch(f'SELECT pl_name, '
                           'pl_bmasse, '
                           'pl_rade, '
                           'pl_dens,'
                           'pl_orbper, '
                           'disc_year, disc_pubdate, '
                           'discoverymethod, '
                           'hostname, '
                           'rastr, '
                           'decstr, '
                           'sy_plx, '
                           'sy_dist * 3.26156 as sy_dist_ly, '
                           'sy_dist, '
                           'st_mass, '
                           'st_rad, '
                           'st_teff, '
                           'st_spectype, '
                           'sy_pnum, '
                           f'sy_snum, '
                           f'st_lum FROM \"PSCompPars\" WHERE pl_name = \'{nome}\'')
            response = [dict(r) for r in row]
            return response
        except Exception as e:
            print(f'Erro: {e}')
        finally:
            await db.close()
    
    async def buscar_todos_exoplanetas_v2(self, offset=0) -> list:
        db = await self.__conn2
        try:  
            row = await db.fetch(f'SELECT pl_name, pl_bmasse, sy_dist * 3.26156 as sy_dist_ly FROM \"PSCompPars\" WHERE pl_name IS NOT NULL ORDER BY pl_name ASC LIMIT 10 OFFSET {offset}')
            rows = [dict(r) for r in row]   
            return rows
        except Exception as e:
            print(f'{e}')
        finally:
            await db.close()
    
    async def pesquisar_por_exoplaneta_v2(self, nome: str) -> list:
        db = await self.__conn2
        try:
            row = await db.fetch(f'SELECT pl_name, pl_bmasse, sy_dist * 3.26156 as sy_dist_ly FROM \"PSCompPars\" WHERE pl_name ILIKE \'{nome}%\' ORDER BY pl_name ASC LIMIT 10')
            response = [dict(r) for r in row]
            return response
        except Exception as e:
            print(f'Erro ao buscar exoplaneta: {e}')
        finally:
           await db.close()