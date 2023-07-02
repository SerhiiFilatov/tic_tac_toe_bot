import asyncpg
import logging

from aiogram.filters.state import State, StatesGroup



class FSMFillForm(StatesGroup):
    game_board = State()
    cross_or_toe: str = State()
    game_status = State()



class Database:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.pool = connector

    async def add_user(self, user_id, user_name):
        await self.pool.execute('INSERT INTO users (user_id, user_name) '
                                'VALUES($1, $2)', user_id, user_name)
        logging.info("Пользователь успешно добавлен в базу данных.")

    async def check_user_exists(self, user_id):
        query = 'SELECT EXISTS(SELECT 1 FROM users WHERE user_id = $1)'
        result = await self.pool.fetchval(query, user_id)
        return result

    async def add_win(self, user_id):
        await self.pool.execute('UPDATE users SET user_wins = user_wins + 1 WHERE user_id = $1', user_id)
        logging.info("Win game info added")

    async def add_lose(self, user_id):
        await self.pool.execute('UPDATE users SET user_loses = user_loses + 1 WHERE user_id = $1', user_id)
        logging.info("Lose game info added")

    async def add_game(self, user_id):
        await self.pool.execute('UPDATE users SET user_games = user_games + 1 WHERE user_id = $1', user_id)
        logging.info("Game info added")

    async def info_games(self, user_id):
        '''
        :param user_id: callback.from_user.id
        :return: одну строку результата в виде словаря
        '''
        query = 'SELECT user_games, user_wins, user_loses FROM users WHERE user_id = $1'
        result = await self.pool.fetchrow(query, user_id)
        return result

    async def info_records(self):
        '''
        :return: все строки результата в виде списка словарей
        '''
        query = 'SELECT user_name, user_games, user_wins, user_loses FROM users ORDER BY user_wins DESC'
        result = await self.pool.fetch(query)
        return result

