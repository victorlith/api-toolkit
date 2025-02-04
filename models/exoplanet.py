from database.database_conn import DatabaseConnection


class Exoplanet:
    def __init__(self):
        self.__conn2 = DatabaseConnection().postgre_db()

    async def buscar_exoplaneta_v2(self, nome: str):
        db = await self.__conn2
        try:
            row = await db.fetch(f'''
                SELECT 
                    pl_name,
                    CASE WHEN pl_bmasse IS NULL THEN 0 ELSE pl_bmasse END AS pl_bmasse_s,
                    pl_rade,
                    pl_dens,
                    CASE WHEN pl_orbper IS NULL THEN 0 ELSE pl_orbper END AS pl_orbper_s,
                    disc_year,
                    disc_pubdate,
                    discoverymethod,
                    hostname,
                    rastr,
                    decstr,
                    CASE WHEN sy_plx IS NULL THEN 0 ELSE sy_plx END AS sy_plx_s,
                    CASE WHEN sy_dist IS NULL THEN 0 ELSE sy_dist END AS sy_dist_s,
                    CASE WHEN sy_dist IS NULL THEN 0 ELSE sy_dist * 3.26156 END AS sy_dist_ly,
                    CASE WHEN st_mass IS NULL THEN 0 ELSE st_mass END AS st_mass_s,
                    CASE WHEN st_rad IS NULL THEN 0 ELSE st_rad END AS st_rad_s,
                    st_teff,
                    st_spectype,
                    sy_pnum,
                    sy_snum,
                    st_lum
                FROM "PSCompPars" 
                WHERE pl_name = '{nome}'
            ''')
            response = [dict(r) for r in row]
            return response
        except Exception as e:
            print(f'Erro: {e}')
        finally:
            await db.close()
    
    async def buscar_todos_exoplanetas_v2(self, offset=0) -> list:
        db = await self.__conn2
        try:  
            row = await db.fetch(f'''
                                 SELECT pl_name, 
                                 CASE WHEN pl_bmasse IS NULL THEN 0 ELSE pl_bmasse END AS pl_bmasse, 
                                 CASE WHEN sy_dist IS NULL THEN 0 ELSE sy_dist * 3.26156 END AS sy_dist_ly 
                                 FROM \"PSCompPars\" WHERE pl_name IS NOT NULL ORDER BY pl_name ASC LIMIT 10 OFFSET {offset} ''')
            rows = [dict(r) for r in row]   
            return rows
        except Exception as e:
            print(f'{e}')
        finally:
            await db.close()
    
    async def pesquisar_por_exoplaneta_v2(self, nome: str) -> list:
        db = await self.__conn2
        try:
            row = await db.fetch(f'''SELECT pl_name, 
                                 CASE WHEN pl_bmasse IS NULL THEN 0 ELSE pl_bmasse END AS pl_bmasse, 
                                 CASE WHEN sy_dist IS NULL THEN 0 ELSE sy_dist * 3.26156 END AS sy_dist_ly 
                                 FROM \"PSCompPars\" WHERE pl_name ILIKE \'{nome}%\' ORDER BY pl_name ASC LIMIT 10 ''')
            response = [dict(r) for r in row]
            return response
        except Exception as e:
            print(f'Erro ao buscar exoplaneta: {e}')
        finally:
           await db.close()