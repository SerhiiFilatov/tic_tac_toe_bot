import logging

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

import game_engine as eng
from game_data import get_field_matrix
from bot_database.database import FSMFillForm, Database
from bot_keaboards.callback_keaboards import get_field_keyboard, GameBoardCallbackFactory, \
                                             menu_buttons, new_game_button, new_game_button_2


router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, request: Database):
    await message.answer(text='TIC-TAC-TOE', reply_markup=menu_buttons)
    if await request.check_user_exists(message.from_user.id):
        pass
    else:
        await request.add_user(message.from_user.id, message.from_user.username)


@router.callback_query(Text("new_game"))
async def process_start_command(callback: CallbackQuery, state: FSMContext, request: Database):
    reset_field = get_field_matrix()
    game_status = True
    await request.add_game(callback.from_user.id)
    await state.set_state(FSMFillForm.cross_or_toe)
    await state.update_data(cross_or_toe='cross')
    await state.set_state(FSMFillForm.game_board)
    await state.update_data(game_board=reset_field)
    await state.set_state(FSMFillForm.game_status)
    await state.update_data(game_status=True)
    datakey = await state.get_data()
    await callback.message.edit_text(text=f'Hello, {callback.from_user.username or callback.from_user.id}',
                                     reply_markup=get_field_keyboard(datakey, game_status))


@router.callback_query(GameBoardCallbackFactory.filter())
async def process_game(callback: CallbackQuery, callback_data: GameBoardCallbackFactory, state: FSMContext,
                       request: Database):

    datakey = await state.get_data()
    field = datakey['game_board']
    player_letter = 1 if datakey['cross_or_toe'] == 'cross' else 2
    bot_letter = 1 if datakey['cross_or_toe'] == 'toe' else 2
    game_status = True
    turn = eng.turn_move(player_letter)

    while game_status:

        if turn == 'player':

            if field[callback_data.x][callback_data.y] == 0:
                field[callback_data.x][callback_data.y] = player_letter
                await state.update_data(game_board=field)
                logging.info(field)
            elif eng.is_winner(let=player_letter, g_f=field):
                game_status = False
                await callback.answer(text='player win')
                await callback.message.edit_reply_markup(reply_markup=get_field_keyboard(datakey, game_status))
                await request.add_win(callback.from_user.id)
            elif eng.full_board(field):
                game_status = False
                await callback.answer(text='draw')
                await callback.message.edit_reply_markup(reply_markup=get_field_keyboard(datakey, game_status))
            else:
                await callback.message.edit_reply_markup(reply_markup=get_field_keyboard(datakey, game_status))
                turn = 'bot'

        else:
            coordinates = eng.bot_move(game_field=field, bot_letter=bot_letter, player_letter=player_letter)
            field[coordinates[0]][coordinates[1]] = bot_letter
            await state.update_data(game_board=field)

            if eng.is_winner(let=bot_letter, g_f=field):
                game_status = False
                await request.add_lose(callback.from_user.id)
                await callback.message.edit_reply_markup(reply_markup=get_field_keyboard(datakey, game_status))
                await callback.answer(text='bot win')
            elif eng.full_board(field):
                game_status = False
                await callback.message.edit_reply_markup(reply_markup=get_field_keyboard(datakey, game_status))
            else:
                await callback.message.edit_reply_markup(reply_markup=get_field_keyboard(datakey, game_status))
                turn = 'player'

    await callback.answer()


@router.callback_query((F.data == 'exit'), ~StateFilter(default_state))
async def process_exit_command(callback: CallbackQuery):
    await callback.message.edit_text(text='Hello world', reply_markup=menu_buttons)


@router.callback_query(F.data == 'stats')
async def process_help_command(callback: CallbackQuery, request: Database):
    stats = await request.info_games(callback.from_user.id)
    player = 'player'
    games = stats[0] or 0
    wins = stats[1]
    loses = stats[2]
    await callback.message.edit_text(text=f'<pre>Player: {callback.from_user.username or player}\nGames: '
                                          f'{games}\nWins: '
                                          f'{wins}\nLosses: {loses}</pre>', parse_mode="HTML",
                                          reply_markup=new_game_button)


@router.callback_query(F.data == 'records')
async def process_help_command(callback: CallbackQuery, request: Database):
    stats = await request.info_records()
    table_text = f"{'User Name': <10} {'Games': <5} {'Wins': <5} {'Losses': <5}\n"
    table_text += "-" * 29 + "\n"
    for row in stats:
        user_name = row[0] or 'player'
        user_games = row[1]
        user_wins = row[2]
        user_loses = row[3]
        table_text += f"{user_name: <12} {user_games: <5} {user_wins: <5} {user_loses: <5}\n"
    await callback.message.edit_text(text=f"<pre>{table_text}</pre>", parse_mode="HTML",
                                     reply_markup=new_game_button_2)