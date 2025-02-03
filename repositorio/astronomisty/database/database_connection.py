import asyncio

import asyncpg

class DatabaseConnection:
    def __init__(self):
        self.db_config = {
            'database': 'astroplanet',
            'user': 'victor',  # Substitua pelo seu usuário
            'password': 'S@bedoria10',  # Substitua pela sua senha
            'host': '194.163.148.45',
            'port': 5432
        }

    async def db_connection(self):
        return await asyncpg.connect(**self.db_config)


if __name__ == '__main__':
    db = DatabaseConnection()
    asyncio.run(db.db_connection())